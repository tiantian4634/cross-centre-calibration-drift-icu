# -*- coding: utf-8 -*-
"""
路B · 分析 I：分层收缩重校准能否解决「小样本重校准负收益」？
========================================
【预注册】先写下设计与判据（写入 03_统计\\分析计划_分析I.md）——**先于任何结果计算**：

  动机：结果 E 显示朴素重校准在 m=25 时比不校准更糟（噪声 > 信号）。
        本分析检验：把各中心的偏移估计**向合并均值做经验贝叶斯收缩**，能否在小样本下翻盘。

  四种策略（在同一 (h, m, rep) 抽样上比较，评估集为该院剩余患者）：
    S0  不重校准（原样移植外部模型）
    S1  朴素：仅重估截距（a_MLE）
    S2  朴素：截距 + 校准斜率
    S3  **分层收缩（EB）**：a_EB = ā + λ·(a_MLE − ā)，λ = τ²/(τ² + se²)
        其中 ā 与 τ² 由**其余全部中心**（leave-one-hospital-out）估计，
        避免用该院自身评估集信息（LOO 交叉拟合，不泄漏）

  指标（与 结果 E 同口径，便于直接对比）：
    R1 残余 |a| 中位数与 P90
    R2 每次重抽样 |O/E−1| ≤10%（或 ≤20%）的比例，再对中心取平均

  **判据（事前设定）**：若在 m=25 时 S3 的 ±10% 达标率显著高于 S1
      （配对比较，双侧），且在 m≥100 时 S3 不劣于 S1（差值 > −5 个百分点），
      则「分层收缩是可行的改进」成立。

  措辞红线：本分析提出的是一条**统计学上的改进建议**，
            不构成临床推荐；tau² 的 LOO 估计仍基于同一批 eICU 中心。
"""
import io, sys, os, json, datetime
import numpy as np, pandas as pd
from scipy.special import expit, logit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
ST, FG = os.path.join(SRCDIR, "03_统计"), os.path.join(SRCDIR, "04_图表")
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
PRE = open(os.path.join(SRCDIR, "analysis_shrinkage.py.pre"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(SRCDIR, "analysis_shrinkage.py.pre")) else None
_write_prereg(os.path.join(ST, "分析计划_分析I.md"), 
    __doc__.replace('"""', "") + f"\n\n> 生成：{ts}（先于结果）\n")
print("[pre-reg] 已写入 分析计划_分析I.md")

# ---------------- 数据与外部模型（同 analysis_drift 口径：SOFA 单评分） ----------------
hid = pd.read_csv(os.path.join(SRCDIR, "hospital_id_map.csv"))
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv")).merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int)
mu, sd = E["sofa"].mean(), E["sofa"].std()
from sklearn.linear_model import LogisticRegression
mp = LogisticRegression(max_iter=5000, C=1.0).fit(((E[["sofa"]].values - mu) / sd), E["y"].values)
E["p"] = mp.predict_proba((E[["sofa"]].values - mu) / sd)[:, 1]
E["lp"] = logit(np.clip(E["p"].values, 1e-8, 1 - 1e-8))
# 只保留探测轮定义的可算中心（n≥100 且死亡≥10）
H0 = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
keep = set(H0[H0["score"] == "SOFA"]["hospital"].tolist())
E = E[E["hospitalid"].isin(keep)].copy()
groups = {h: (g["lp"].values, g["y"].values) for h, g in E.groupby("hospitalid")}
print(f"[data] 中心 k={len(groups)}；患者 {len(E):,}")


def solve_a(lp, y):
    obs = y.mean(); lo, hi = -12.0, 12.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if expit(lp + mid).mean() < obs: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def dersimonian(a, se):
    """DL 估计 τ²，并返回**随机效应加权**的合并均值供 EB 收缩使用。

    权重分工（不可混用）：
      · w = 1/se²       → 计算 Q 与 τ²（DerSimonian-Laird 的定义，固定效应权重）
      · w = 1/(se²+τ²)  → 计算返回的合并均值
    为何必须用后者：收缩公式 a_EB = ā + λ(a − ā) 中 λ = τ²/(τ²+se²) 来自
    层次模型 a ~ N(ā, τ²+se²)，该模型下 ā 的极大似然估计正是随机效应加权均值。
    若 ā 用固定效应权重（等价于假设 τ² = 0），则与 λ 假设 τ² > 0 自相矛盾。
    """
    a, se = np.asarray(a, float), np.asarray(se, float)
    w = 1.0 / se ** 2
    abar_fe = np.sum(w * a) / np.sum(w)
    Q = np.sum(w * (a - abar_fe) ** 2)
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (len(a) - 1)) / C)
    wr = 1.0 / (se ** 2 + tau2)
    return np.sum(wr * a) / np.sum(wr), tau2


def se_of_a(p, y, a):
    pp = expit(logit(np.clip(np.asarray(p, float), 1e-8, 1 - 1e-8)) + a)
    obs = y.mean()
    return np.sqrt(max(obs * (1 - obs), 1e-9) / len(y)) / max(float(np.mean(pp * (1 - pp))), 1e-9)


# 全量数据上每中心的 (a_full, se_full) —— 供 LOO 估计 ā, τ²
full = {h: (solve_a(lp, y), se_of_a(expit(lp), y, solve_a(lp, y)), len(y))
        for h, (lp, y) in groups.items()}
ah = np.array([full[h][0] for h in groups]); seh = np.array([full[h][1] for h in groups])
abar_all, tau_all = dersimonian(ah, seh)
print(f"[pooled] ā(RE加权·收缩目标) = {abar_all:+.4f}；τ² = {tau_all:.4f}（k={len(ah)}）")

MS = [0, 25, 50, 100, 200]; NREP = 200
recs = []
for hi, h in enumerate(groups):
    lp, y = groups[h]
    n = len(lp)
    # LOO：用其余中心估计 ā, τ²
    a_o = np.delete(ah, hi); se_o = np.delete(seh, hi)
    a_bar_loo, tau_loo = dersimonian(a_o, se_o)
    tau_loo = max(tau_loo, 1e-6)
    for m in MS:
        if m > 0 and n < 2 * m:
            continue
        if m == 0:
            a0 = solve_a(lp, y)
            oe0 = y.mean() / max(expit(lp).mean(), 1e-9)
            for s in ["S0", "S1", "S2", "S3"]:
                recs.append(dict(h=h, m=0, rep=0, strat=s, resid_a=abs(a0), oe=oe0))
            continue
        for rep in range(NREP):
            rng = np.random.default_rng(20261019 + rep * 9973 + hi * 131)
            idx = rng.choice(n, size=m, replace=False)
            mask = np.ones(n, bool); mask[idx] = False
            lp_c, y_c = lp[idx], y[idx]
            lp_e, y_e = lp[mask], y[mask]
            if len(np.unique(y_c)) < 2 or len(np.unique(y_e)) < 2:
                continue
            # S1 朴素截距
            a1 = solve_a(lp_c, y_c); se1 = se_of_a(expit(lp_c), y_c, a1)
            # S2 朴素截距+斜率
            mm = LogisticRegression(max_iter=5000, C=1e6).fit(lp_c.reshape(-1, 1), y_c)
            b2 = float(mm.coef_[0, 0]); a2 = float(mm.intercept_[0])
            # S3 EB 收缩（shrink 向 LOO 合并均值）
            lam = tau_loo / (tau_loo + se1 ** 2)
            a3 = a_bar_loo + lam * (a1 - a_bar_loo)
            for s, tot_a, tot_b in [("S1", a1, 1.0), ("S2", a2, b2), ("S3", a3, 1.0)]:
                ra = solve_a(lp_e * tot_b + tot_a, y_e)
                oe = y_e.mean() / max(expit(lp_e * tot_b + tot_a).mean(), 1e-9)
                recs.append(dict(h=h, m=m, rep=rep, strat=s, resid_a=abs(ra), oe=oe,
                                 lam=float(lam)))
R = pd.DataFrame(recs)
R["oe_absdev"] = (R["oe"] - 1.0).abs()
R["ok11"] = (R["oe_absdev"] <= 0.10).astype(float)
R["ok12"] = (R["oe_absdev"] <= 0.20).astype(float)
R.to_csv(os.path.join(ST, "shrinkage_raw.csv"), index=False, encoding="utf-8-sig")

print("\n" + "=" * 92)
print("### 分析 I：分层收缩(EB) vs 朴素重校准")
print("=" * 92)
NAME = {"S0": "S0 不重校准", "S1": "S1 朴素·仅截距", "S2": "S2 朴素·截距+斜率", "S3": "S3 EB·收缩截距"}
out = []
for m in MS:
    sub = R[R["m"] == m]
    if sub.empty:
        continue
    print(f"\n-- m = {m} --")
    print(f"   {'策略':<20}{'k':>5}{'残余|a| 中位':>13}{'P90':>8}{'|O/E−1|≤10%':>14}{'≤20%':>9}")
    for s in ["S0", "S1", "S2", "S3"]:
        g = sub[sub["strat"] == s]
        if g.empty:
            continue
        per = g.groupby("h").agg(ra=("resid_a", "median"), ok11=("ok11", "mean"), ok12=("ok12", "mean"))
        k = len(per)
        ra_med, ra_p90 = per["ra"].median(), np.percentile(per["ra"], 90)
        w11, w12 = 100 * per["ok11"].mean(), 100 * per["ok12"].mean()
        print(f"   {NAME[s]:<20}{k:>5}{ra_med:>13.4f}{ra_p90:>8.4f}{w11:>13.1f}%{w12:>8.1f}%")
        out.append(dict(m=m, strat=s, k=k, ra_med=round(ra_med, 4), ra_p90=round(ra_p90, 4),
                        ok11=round(w11, 1), ok12=round(w12, 1)))

# 配对比较：m=25 时 S3 vs S1
sub = R[R["m"] == 25]
piv = sub.pivot_table(index=["h", "rep"], columns="strat", values="ok11")
d = (piv["S3"] - piv["S1"]).dropna()
from scipy.stats import wilcoxon
try:
    wstat, wp = wilcoxon(d)
except Exception:
    wp = np.nan
print(f"\n[配对] m=25 时 S3−S1 达标率差 = {100*d.mean():+.2f} 个百分点"
      f"（配对次数 {len(d)}；Wilcoxon P = {wp:.3g}）")
sub100 = R[R["m"] == 100]
piv2 = sub100.pivot_table(index=["h", "rep"], columns="strat", values="ok11")
d2 = (piv2["S3"] - piv2["S1"]).dropna()
print(f"[配对] m=100 时 S3−S1 达标率差 = {100*d2.mean():+.2f} 个百分点")

# 判据
ok = (100 * d.mean() > 0) and (100 * d2.mean() > -5)
print(f"\n[判据] m=25 S3 优于 S1（>0） 且 m=100 不劣于 5 个百分点 → "
      f"**{'成立' if ok else '不成立'}**")
json.dump(dict(rows=out, lambda_mean=round(float(R[R['m'] > 0]['lam'].mean()), 4),
               paired_m25=round(float(100 * d.mean()), 2), paired_m100=round(float(100 * d2.mean()), 2),
               wilcoxon_p=float(wp), criterion_ok=bool(ok)),
          open(os.path.join(ST, "shrinkage_summary.json"), "w", encoding="utf-8"), indent=2)
print("[done] ->", ST)
