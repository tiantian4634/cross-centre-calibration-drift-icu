# -*- coding: utf-8 -*-
"""
路B · 分析 J：EB 收缩方案在 MIMIC-IV 上的外部验证
========================================
【预注册】先写下设计与判据（写入 03_统计\\分析计划_分析J.md）——**先于任何结果计算**：

  问题：分析 I 提出的分层收缩方案，其**收缩目标 ā 与 院间方差 τ² 全部由 eICU 估计**。
        换到一个完全不同的数据库（MIMIC-IV，美国另一家学术医疗中心、不同年份、
        不同医院体系），这套参数还管用吗？

  设计：
    · 外部模型 = eICU 全量拟合的 SOFA 单评分 logistic（用 eICU 的标准化参数投影）
    · 收缩参数 **固定取自 eICU**（k=103 家医院的随机效应估计）：ā_eicu、τ²_eicu
      —— **绝不在 MIMIC 上重估**，否则不构成外部验证
    · MIMIC-IV 的 8,579 例整体视为「一个新中心」，其相对外部模型的真实偏移
      a*_MIMIC 已知（由全量计算），作为待恢复的真值
    · 对 m ∈ {25, 50, 100, 200, 400}：从 MIMIC 随机抽 m 例作"本地校准集"，
      其余作评估集；重复 200 次；要求 n ≥ 2m
    · 比较：
        S0  不重校准
        S1  朴素仅截距（a_MLE，由 m 例估）
        S3  **EB 收缩**：a_EB = ā_eicu + λ(a_MLE − ā_eicu)，λ = τ²_eicu/(τ²_eicu + se²)
    · 指标同分析 I：残余 |a|；每次重抽样 |O/E−1| ≤10% / ≤20% 的比例

  **判据（事前设定）**：在 m=25 时，S3 的 ±10% 达标率 **> S1** 且 **> S0（不校准）**；
        并报告 m 各档的差值与配对检验。

  措辞红线：
    · MIMIC 为**单中心**，本分析验证的是「收缩参数能否跨数据库迁移」，
      **不是**「方案在多中心环境下的表现」（后者只能由 eICU 自身的 LOO 完成）。
    · 两者须在论文中明确区分，不得混称"外部多中心验证"。
"""
import io, sys, os, json, datetime
import numpy as np, pandas as pd
from scipy.special import expit, logit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def _write_prereg(path, text):
    """幂等写入预注册文档：已存在则不覆盖，以保住『先于结果』的原始时间戳。"""
    if os.path.exists(path):
        print(f"[pre-reg] {os.path.basename(path)} 已存在，保留原始时间戳，不覆盖")
    else:
        open(path, "w", encoding="utf-8").write(text)
        print(f"[pre-reg] 已写入 {os.path.basename(path)}")
np.random.seed(20261019)

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
SRCDIR = os.path.join(BASE, "09_路B_跨院校准")
ST = os.path.join(SRCDIR, "03_统计")
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
_write_prereg(os.path.join(ST, "分析计划_分析J.md"), 
    __doc__.replace('"""', "") + f"\n\n> 生成：{ts}（先于结果）\n")
print("[pre-reg] 已写入 分析计划_分析J.md")

# ---------- eICU 侧：外部模型 + 固定的收缩参数 ----------
hid = pd.read_csv(os.path.join(SRCDIR, "hospital_id_map.csv"))
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv")).merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int)
mu, sd = E["sofa"].mean(), E["sofa"].std()
mp = LogisticRegression(max_iter=5000, C=1.0).fit(((E[["sofa"]].values - mu) / sd), E["y"].values)
DR = json.load(open(os.path.join(ST, "drift_results.json"), encoding="utf-8"))
ABAR = DR["scores"]["SOFA"]["a_bar"]; TAU2 = DR["scores"]["SOFA"]["tau2"]
print(f"[eICU 固定收缩参数] ā = {ABAR:+.4f}；τ² = {TAU2:.4f}（k={DR['scores']['SOFA']['k']} 家医院）")

# ---------- MIMIC 侧：作为一个"新中心" ----------
M = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_mimiciv.csv")).dropna(
    subset=["sofa", "age", "male", "hosp_death"]).copy()
M["y"] = M["hosp_death"].astype(int)
M["p"] = mp.predict_proba(((M[["sofa"]].values - mu) / sd))[:, 1]
M["lp"] = logit(np.clip(M["p"].values, 1e-8, 1 - 1e-8))
lp, y = M["lp"].values, M["y"].values
n = len(M)


def solve_a(lpv, yv):
    obs = yv.mean(); lo, hi = -12.0, 12.0
    for _ in range(120):
        mid = (lo + hi) / 2
        if expit(lpv + mid).mean() < obs: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def se_of_a(lpv, yv, a):
    pp = expit(lpv + a)
    return np.sqrt(max(yv.mean() * (1 - yv.mean()), 1e-9) / len(yv)) / max(float(np.mean(pp * (1 - pp))), 1e-9)


a_star = solve_a(lp, y)
print(f"\n[MIMIC 作为新中心] n = {n:,}；事件 {y.sum():,}（{100*y.mean():.2f}%）")
print(f"  外部模型在 MIMIC 上的 AUC = {roc_auc_score(y, expit(lp)):.4f}")
print(f"  观测死亡率 {100*y.mean():.1f}%  vs  模型预测均值 {100*expit(lp).mean():.1f}%  "
      f"O/E = {y.mean()/expit(lp).mean():.2f}")
print(f"  **MIMIC 的真实校准偏移 a* = {a_star:+.4f}**（待恢复的真值）")

MS = [0, 25, 50, 100, 200, 400]; NREP = 200
recs = []
for m in MS:
    if m > 0 and n < 2 * m:
        continue
    if m == 0:
        for s in ["S0", "S1", "S3"]:
            recs.append(dict(m=0, rep=0, strat=s, resid_a=abs(a_star),
                             oe=y.mean() / max(expit(lp).mean(), 1e-9)))
        continue
    for rep in range(NREP):
        rng = np.random.default_rng(20261019 + rep * 9973 + m)
        idx = rng.choice(n, size=m, replace=False)
        mask = np.ones(n, bool); mask[idx] = False
        lp_c, y_c, lp_e, y_e = lp[idx], y[idx], lp[mask], y[mask]
        if len(np.unique(y_c)) < 2 or len(np.unique(y_e)) < 2:
            continue
        a1 = solve_a(lp_c, y_c); se1 = se_of_a(lp_c, y_c, a1)
        lam = TAU2 / (TAU2 + se1 ** 2)
        a3 = ABAR + lam * (a1 - ABAR)
        for s, tot in [("S1", a1), ("S3", a3)]:
            ra = solve_a(lp_e + tot, y_e)
            oe = y_e.mean() / max(expit(lp_e + tot).mean(), 1e-9)
            recs.append(dict(m=m, rep=rep, strat=s, resid_a=abs(ra), oe=oe, lam=float(lam)))
R = pd.DataFrame(recs)
R["oe_absdev"] = (R["oe"] - 1).abs()
R["ok11"] = (R["oe_absdev"] <= 0.10).astype(float)
R["ok12"] = (R["oe_absdev"] <= 0.20).astype(float)
R.to_csv(os.path.join(ST, "mimic_external_raw.csv"), index=False, encoding="utf-8-sig")

print("\n" + "=" * 88)
print("### 分析 J：EB 收缩方案在 MIMIC-IV 上的外部验证（收缩参数固定来自 eICU）")
print("=" * 88)
NAME = {"S0": "S0 不重校准", "S1": "S1 朴素·仅截距", "S3": "S3 EB·收缩（eICU 参数）"}
out = []
for m in MS:
    sub = R[R["m"] == m]
    if sub.empty:
        continue
    print(f"\n-- m = {m} --")
    print(f"   {'策略':<28}{'残余|a| 中位':>13}{'P90':>8}{'|O/E−1|≤10%':>14}{'≤20%':>9}")
    for s in ["S0", "S1", "S3"]:
        g = sub[sub["strat"] == s]
        if g.empty:
            continue
        ra_med = g["resid_a"].median(); ra_p90 = np.percentile(g["resid_a"], 90)
        w11, w12 = 100 * g["ok11"].mean(), 100 * g["ok12"].mean()
        print(f"   {NAME[s]:<28}{ra_med:>13.4f}{ra_p90:>8.4f}{w11:>13.1f}%{w12:>8.1f}%")
        out.append(dict(m=m, strat=s, ra_med=round(ra_med, 4), ra_p90=round(ra_p90, 4),
                        ok11=round(w11, 1), ok12=round(w12, 1)))
    if m > 0:
        piv = sub.pivot_table(index="rep", columns="strat", values="ok11")
        if "S1" in piv and "S3" in piv:
            d = (piv["S3"] - piv["S1"]).dropna()
            from scipy.stats import wilcoxon
            try:
                wp = wilcoxon(d)[1]
            except Exception:
                wp = np.nan
            print(f"   [配对] S3−S1 = {100*d.mean():+.2f} 个百分点（配对 {len(d)} 次；P = {wp:.3g}）")
            out[-1]["paired_S3_S1"] = round(float(100 * d.mean()), 2)
            out[-1]["paired_p"] = float(wp)

d25 = [o for o in out if o["m"] == 25]
s1_25 = [o for o in d25 if o["strat"] == "S1"][0]["ok11"]
s3_25 = [o for o in d25 if o["strat"] == "S3"][0]["ok11"]
s0 = [o for o in out if o["m"] == 0][0]["ok11"]
ok = (s3_25 > s1_25) and (s3_25 > s0)
print(f"\n[判据] m=25：S3 ({s3_25}%) > S1 ({s1_25}%) 且 > S0 不校准 ({s0}%) → "
      f"**{'成立' if ok else '不成立'}**")
json.dump(dict(a_star=round(float(a_star), 4), n=n, events=int(y.sum()),
               auc=round(float(roc_auc_score(y, expit(lp))), 4),
               abar_eicu=ABAR, tau2_eicu=TAU2, rows=out, criterion_ok=bool(ok)),
          open(os.path.join(ST, "mimic_external_summary.json"), "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("[done] ->", ST)
