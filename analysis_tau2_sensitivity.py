# -*- coding: utf-8 -*-
"""
路B · 分析 K（修正版）：τ² 框架敏感性 —— EB 收缩结论是否依赖 τ² 的估计路径？
========================================
背景（诚实记录）：
  · 首轮误把 statsmodels `exp(vcp_mean)` 当作方差；读源码确认其为**标准差**
    （bayes_mixed_glm.py L303-305: "standard deviation for random effect j is exp(vcp[ident[j]])"）。
    正确的多水平 τ² = exp(vcp_mean)² = 0.2470² = **0.0610**，而非首轮报的 0.2545。
  · 校正后：两阶段 meta 分析 τ² ≈ 0.13，一阶段多水平/边际似然 τ² ≈ 0.06–0.07，仍差约 2 倍。

本分析只回答一个问题：**换用更低的 τ²，EB 收缩是否仍然优于朴素重校准？**
"""
import io, sys, os, json
import numpy as np, pandas as pd
from scipy.special import expit, logit
from scipy.stats import wilcoxon
from sklearn.linear_model import LogisticRegression

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
np.random.seed(20261019)
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
SRCDIR = os.path.join(BASE, "09_路B_跨院校准"); ST = os.path.join(SRCDIR, "03_统计")

hid = pd.read_csv(os.path.join(SRCDIR, "hospital_id_map.csv"))
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv")).merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int)
mu, sd = E["sofa"].mean(), E["sofa"].std()
mp = LogisticRegression(max_iter=5000, C=1.0).fit(((E[["sofa"]].values - mu) / sd), E["y"].values)
E["p"] = mp.predict_proba((E[["sofa"]].values - mu) / sd)[:, 1]
E["lp"] = logit(np.clip(E["p"].values, 1e-8, 1 - 1e-8))
H0 = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
keep = set(H0[H0["score"] == "SOFA"]["hospital"].tolist())
E = E[E["hospitalid"].isin(keep)].copy()
groups = {h: (g["lp"].values, g["y"].values) for h, g in E.groupby("hospitalid")}
print(f"[data] k={len(groups)}；n={len(E):,}")


def solve_a(lpv, yv):
    obs = yv.mean(); lo, hi = -12.0, 12.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if expit(lpv + mid).mean() < obs: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def se_of_a(pv, yv, a):
    pp = expit(logit(np.clip(pv, 1e-8, 1 - 1e-8)) + a)
    return np.sqrt(max(yv.mean() * (1 - yv.mean()), 1e-9) / len(yv)) / max(float(np.mean(pp * (1 - pp))), 1e-9)


# 三个候选 τ²（DL 两阶段 / 手工边际似然 / 多水平 MAP·校正后）
TAUS = {"τ²=0.131 (DL, 两阶段)": 0.1312,
        "τ²=0.071 (边际似然 ML)": 0.0706,
        "τ²=0.061 (多水平 MAP)": 0.0610}
ABAR = 0.030   # 随机效应加权合并均值（τ²≈0.13 时）；τ² 变化时按 RE 权重重算
MS = [25, 50, 100, 200]
NREP = 100

full = {h: solve_a(lp, y) for h, (lp, y) in groups.items()}
se_full = {h: se_of_a(expit(lp), y, full[h]) for h, (lp, y) in groups.items()}

out = {}
for tname, TAU2 in TAUS.items():
    ah = np.array([full[h] for h in groups]); seh = np.array([se_full[h] for h in groups])
    w = 1.0 / (seh ** 2 + TAU2); abar_t = float(np.sum(w * ah) / np.sum(w))
    recs = []
    for hi, h in enumerate(groups):
        lp, y = groups[h]; n = len(lp)
        for m in MS:
            if n < 2 * m:
                continue
            for rep in range(NREP):
                rng = np.random.default_rng(20261019 + rep * 7919 + hi)
                idx = rng.choice(n, size=m, replace=False)
                mask = np.ones(n, bool); mask[idx] = False
                lp_c, y_c, lp_e, y_e = lp[idx], y[idx], lp[mask], y[mask]
                if len(np.unique(y_c)) < 2 or len(np.unique(y_e)) < 2:
                    continue
                a1 = solve_a(lp_c, y_c); se1 = se_of_a(expit(lp_c), y_c, a1)
                lam = TAU2 / (TAU2 + se1 ** 2)
                a3 = abar_t + lam * (a1 - abar_t)
                for s, tot in [("S1", a1), ("S3", a3)]:
                    ra = solve_a(lp_e + tot, y_e)
                    oe = y_e.mean() / max(expit(lp_e + tot).mean(), 1e-9)
                    recs.append(dict(h=h, m=m, rep=rep, strat=s,
                                     ok11=float(abs(oe - 1) <= 0.10), lam=lam))
    R = pd.DataFrame(recs)
    row = {}
    for m in MS:
        g = R[R["m"] == m]
        s1 = g[g["strat"] == "S1"]; s3 = g[g["strat"] == "S3"]
        if s1.empty:
            continue
        row[m] = dict(S1=round(100 * s1["ok11"].mean(), 1), S3=round(100 * s3["ok11"].mean(), 1),
                      lam=round(float(s3["lam"].median()), 3),
                      diff=round(100 * (s3["ok11"].mean() - s1["ok11"].mean()), 1),
                      n=len(s1))
        piv = g.pivot_table(index=["h", "rep"], columns="strat", values="ok11")
        d = (piv["S3"] - piv["S1"]).dropna()
        row[m]["p"] = float(wilcoxon(d)[1]) if len(d) else np.nan
    out[tname] = dict(abar=round(abar_t, 4), tau2=TAU2, by_m=row)

print("\n" + "=" * 86)
print("### 分析 K（修正版）：EB 收缩结论是否依赖 τ² 的估计路径？")
print("=" * 86)
for tname, d in out.items():
    print(f"\n-- {tname}   （RE 加权合并均值 ā = {d['abar']:+.4f}）--")
    print(f"   {'m':>5}{'S1 朴素':>10}{'S3 EB':>10}{'差值':>10}{'λ中位':>8}{'Wilcoxon P':>14}")
    for m in MS:
        r = d["by_m"].get(m)
        if not r:
            continue
        print(f"   {m:>5}{r['S1']:>9.1f}%{r['S3']:>9.1f}%{r['diff']:>+9.1f}{r['lam']:>8.3f}{r['p']:>14.3g}")

ok_all = all(d["by_m"][25]["S3"] > d["by_m"][25]["S1"] for d in out.values() if 25 in d["by_m"])
print(f"\n[判据] 三种 τ² 取值下，m=25 时 EB 均优于朴素 → **{'成立：结论对 τ² 估计路径稳健' if ok_all else '不成立'}**")
json.dump({k: dict(abar=v["abar"], tau2=v["tau2"], by_m={str(m): r for m, r in v["by_m"].items()})
           for k, v in out.items()},
          open(os.path.join(ST, "tau2_sensitivity.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("[done]")
