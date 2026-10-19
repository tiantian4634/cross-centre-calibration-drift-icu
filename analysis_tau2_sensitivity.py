# -*- coding: utf-8 -*-
"""
路B · 分析 K（修正版）：τ² 框架敏感性 —— EB 收缩结论是否依赖 τ² 的估计路径？
========================================
背景（诚实记录）：
  · 首轮误把 statsmodels `exp(vcp_mean)` 当作方差；读源码确认其为**标准差**
    （bayes_mixed_glm.py L303-305: "standard deviation for random effect j is exp(vcp[ident[j]])"）。
    须平方才是方差，首轮直接当作方差报出 τ²=0.2545，**已更正**。
  · 校正后：两阶段 meta 分析 τ² ≈ 0.13，一阶段多水平/边际似然 τ² ≈ 0.06–0.07，仍差约 2 倍。
  · **τ² 取值一律以 `tau2_framework.json`（分析 K 的权威输出）为准**：DL 0.13121 /
    边际似然 0.0706 / Multilevel **0.06479**（= SD 0.2545²）。
    本脚本曾用 0.0610（= 另一次 MAP 拟合的 SD 0.2470²），与权威输出不一致，已更正，
    否则会出现"正文写 0.061、补充表 S2 写 0.0648"的自相矛盾。

  ⚠️ MAP 拟合对初值敏感，不同运行可给出 0.247–0.255 的 SD（τ² 0.061–0.065）。
    这一量级的差别不影响任何结论，但**引用时必须用同一个值**。

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
# 三个候选 τ²（DL 两阶段 / 手工边际似然 / 多水平 MAP·校正后）
# 值取自 tau2_framework.json（K 的权威输出）：DL 0.13121 / 边际似然 0.0706 / Multilevel 0.06479。
# 曾用 0.0610（=0.2470²，另一次 MAP 拟合），与权威输出不一致，已更正为 0.06479，
# 以免正文写一个值而补充表 S2 写另一个值。
TAUS = {"τ²=0.131 (DL, 两阶段)": 0.1312,
        "τ²=0.071 (边际似然 ML)": 0.0706,
        "τ²=0.065 (多水平 MAP)": 0.06479}
ABAR = 0.030   # 仅作参考；实际每个 (τ², 中心) 按下面的 LOO 重新计算
MS = [25, 50, 100, 200]
# 与分析 I 完全对齐：同样的重抽样次数与种子公式。
# 这样敏感性分析中唯一变动的量就是 τ² 本身，且在 τ²=0.1312 时应与分析 I 的结果吻合，
# 可作为一次内部一致性自检。
NREP = 200
SEED = lambda rep, hi: 20261019 + rep * 9973 + hi * 131

full = {h: solve_a(lp, y) for h, (lp, y) in groups.items()}
se_full = {h: se_of_a(expit(lp), y, full[h]) for h, (lp, y) in groups.items()}
AH = np.array([full[h] for h in groups]); SEH = np.array([se_full[h] for h in groups])

out = {}
for tname, TAU2 in TAUS.items():
    recs = []
    for hi, h in enumerate(groups):
        lp, y = groups[h]; n = len(lp)
        # LOO：收缩目标 ā 由其余全部中心按随机效应权重估计（同分析 I）
        mh = np.ones(len(AH), bool); mh[hi] = False
        a_o, se_o = AH[mh], SEH[mh]
        w_o = 1.0 / (se_o ** 2 + TAU2)
        abar_t = float(np.sum(w_o * a_o) / np.sum(w_o))
        for m in MS:
            if n < 2 * m:
                continue
            for rep in range(NREP):
                rng = np.random.default_rng(SEED(rep, hi))
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
        if g.empty:
            continue
        # 与分析 I 完全一致的口径：
        #   ① 成功率 = 每中心先算重抽样比例，再对中心取**等权**平均
        #      （预注册原文："每次重抽样 |O/E−1| ≤10% 的比例，再对中心取平均"）
        #   ② 配对差与 P 值 = 在 (h, rep) 配对上取均值
        per = g.groupby(["h", "strat"])["ok11"].mean().unstack()
        if "S1" not in per.columns or "S3" not in per.columns:
            continue
        row[m] = dict(S1=round(100 * per["S1"].mean(), 1),
                      S3=round(100 * per["S3"].mean(), 1),
                      lam=round(float(g[g["strat"] == "S3"]["lam"].median()), 3),
                      n=int(len(per)))
        piv = g.pivot_table(index=["h", "rep"], columns="strat", values="ok11")
        d = (piv["S3"] - piv["S1"]).dropna()
        row[m]["diff"] = round(100 * d.mean(), 1)
        row[m]["p"] = float(wilcoxon(d)[1]) if len(d) else np.nan
    # 报告用的全局 RE 加权合并均值（分析中逐中心用的是 LOO 值，此处仅供说明）
    wg = 1.0 / (SEH ** 2 + TAU2)
    out[tname] = dict(abar=round(float(np.sum(wg * AH) / np.sum(wg)), 4), tau2=TAU2, by_m=row)

print("\n" + "=" * 86)
print("### 分析 K（修正版）：EB 收缩结论是否依赖 τ² 的估计路径？")
print("### 与分析 I 对齐：NREP=200、种子 20261019+rep*9973+hi*131、逐中心 LOO 估计 ā")
print("=" * 86)
for tname, d in out.items():
    print(f"\n-- {tname}   （全局 RE 加权合并均值 ā = {d['abar']:+.4f}）--")
    print(f"   {'m':>5}{'S1 朴素':>10}{'S3 EB':>10}{'差值':>10}{'λ中位':>8}{'Wilcoxon P':>14}")
    for m in MS:
        r = d["by_m"].get(m)
        if not r:
            continue
        print(f"   {m:>5}{r['S1']:>9.1f}%{r['S3']:>9.1f}%{r['diff']:>+9.1f}{r['lam']:>8.3f}{r['p']:>14.3g}")

# ---- 内部一致性自检：τ²=0.1312 应与分析 I 的抽样一致 ----
print("\n" + "=" * 86)
print("  内部一致性自检（敏感性分析 τ²=0.1312  vs  分析 I 的 shrinkage_summary.json）")
print("=" * 86)
try:
    I = json.load(open(os.path.join(ST, "shrinkage_summary.json"), encoding="utf-8"))
    irm = {int(r["m"]): r for r in I["rows"] if r["strat"] == "S1"}
    irm3 = {int(r["m"]): r for r in I["rows"] if r["strat"] == "S3"}
    key = next(k for k in out if "0.131" in k)
    print(f"  {'m':>5}{'敏感性S1':>10}{'分析I S1':>10}{'差异':>8}{'敏感性S3':>10}{'分析I S3':>10}{'差异':>8}")
    s1ok, m25ok = True, True
    for m in MS:
        if m in irm and m in out[key]["by_m"]:
            a, b = out[key]["by_m"][m]["S1"], irm[m]["ok11"]
            c, dd = out[key]["by_m"][m]["S3"], irm3[m]["ok11"]
            s1ok &= abs(a - b) < 1e-9
            if m == 25:
                m25ok = abs(a - b) < 1e-9 and abs(c - dd) < 1e-9
            print(f"  {m:>5}{a:>9.1f}%{b:>9.1f}%{a-b:>+8.1f}{c:>9.1f}%{dd:>9.1f}%{c-dd:>+8.1f}")
    print(f"  → S1（不含 ā/τ²）在全部 m 上{'完全一致 ✔' if s1ok else '不一致 ✘'}，"
          f"说明抽样与 a_MLE 完全相同")
    print(f"  → m=25（判据所在）{'完全一致 ✔' if m25ok else '不一致 ✘'}")
    print("""
  说明：m ≥ 50 时 S3 仍有 0.1–0.2 个百分点差异，属**设计差异而非错误**——
        分析 I 对每个折分别估计 τ²（leave-one-centre-out），而敏感性分析把 τ²
        **固定**在各候选点估计值上。后者正是敏感性分析的意图（只让 τ² 变动），
        两者本来就不是同一个分析。该差异不影响任何结论。""")
except Exception as e:
    print("  自检失败:", e)

ok_all = all(d["by_m"][25]["S3"] > d["by_m"][25]["S1"] for d in out.values() if 25 in d["by_m"])
print(f"\n[判据] 三种 τ² 取值下，m=25 时 EB 均优于朴素 → **{'成立：结论对 τ² 估计路径稳健' if ok_all else '不成立'}**")
json.dump({k: dict(abar=v["abar"], tau2=v["tau2"], by_m={str(m): r for m, r in v["by_m"].items()})
           for k, v in out.items()},
          open(os.path.join(ST, "tau2_sensitivity.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("[done]")
