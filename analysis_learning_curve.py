# -*- coding: utf-8 -*-
"""
路B · 学习曲线：把外部开发的模型校准到本地，需要多少本地患者？
========================================
【预注册】先写下设计（写入 03_统计\\学习曲线_预注册.md）：

  对每家 eICU 中心 h（n ≥ 200）与每个 m ∈ {0, 25, 50, 100, 200}：
    · 要求 n_h ≥ 2m（本地评估集至少与校准集一样大），否则该 (h,m) 组合不纳入，并报告 k
    · 从该院随机抽 m 例作"本地校准集"，其余 N_h − m 例作"本地评估集"
    · 两种校准策略：
        S1  仅重估截距（intercept-only recalibration）
        S2  重估截距 + 校准斜率（two-parameter recalibration）
    · 在评估集上算**残余失校准**：
        R1 = 残余 |校准截距 a|
        R2 = 残余 O/E 落在 [0.9, 1.1] 的中心比例（宽松带 [0.8, 1.2] 一并报）
    · 每个 (h,m) 重复 100 次重抽样

  判据（事前）：报告使 R2 达到 50% 的最小 m（若达不到则写"200 例仍不足"）。

  措辞红线：本分析只回答"**需要多少数据才能把外部模型校准到本地**"，
            不得解读为"各中心质量高低"。
"""
import io, sys, os, json, datetime
import numpy as np, pandas as pd
from scipy.special import expit, logit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
np.random.seed(20261019)

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST, FG = os.path.join(BASE, "03_统计"), os.path.join(BASE, "04_图表")
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
PRE = """# 路B · 学习曲线 预注册
生成：{ts}（先于结果）

| 项 | 设定 |
|---|---|
| 中心纳入 | n ≥ 200；每个 m 要求 n ≥ 2m，否则该 (h,m) 不纳入并报告 k |
| m | 0（不校准，即原样移植）, 25, 50, 100, 200 |
| 策略 | S1 仅重估截距；S2 截距 + 校准斜率 |
| 指标 | R1 残余 \\|a\\| 中位数与 P90；R2 残余 O/E ∈ [0.9,1.1] 的中心比例（另报 [0.8,1.2]） |
| 重复 | 每 (h,m) 重抽样 100 次 |
| 判据 | 报告使 R2 ≥ 50% 的最小 m；达不到则如实写 |

**措辞红线**：只回答"需要多少本地数据才能校准外部模型"，不作中心间优劣归因。
"""
_prereg_path = os.path.join(ST, "学习曲线_预注册.md")
if not os.path.exists(_prereg_path):      # 幂等：已存在则不覆盖，以保住原始写入时间戳
    open(_prereg_path, "w", encoding="utf-8").write(PRE.replace("{ts}", ts))
    print("[pre-reg] 已写入 学习曲线_预注册.md")
else:
    print("[pre-reg] 学习曲线_预注册.md 已存在，保留原始时间戳，不覆盖")

# ---------- 数据（SOFA 模型） ----------
H = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
H = H[H["score"] == "SOFA"]
E = pd.read_csv(os.path.join(r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图",
                             "02_数据集", "cohort_eicu.csv"))
hid = pd.read_csv(os.path.join(BASE, "hospital_id_map.csv"))
E = E.merge(hid, on="stay_id", how="left").dropna(subset=["hospitalid", "sofa"]).copy()
E["y"] = E["hosp_death"].astype(int)
sofa_mu, sofa_sd = E["sofa"].mean(), E["sofa"].std()
# 合并 SOFA 模型（与 analysis_drift 同口径：单评分标准化 logistic）
from sklearn.linear_model import LogisticRegression
Xs = ((E[["sofa"]].values - sofa_mu) / sofa_sd)
m_pool = LogisticRegression(max_iter=5000, C=1.0).fit(Xs, E["y"].values)
E["p"] = m_pool.predict_proba(Xs)[:, 1]
E["lp"] = logit(np.clip(E["p"].values, 1e-8, 1 - 1e-8))

keep = set(H["hospital"].tolist())
E = E[E["hospitalid"].isin(keep)].copy()
print(f"[data] 纳入中心 k={len(keep)}；患者 {len(E):,}")


def solve_a(lp, y):
    """在 m 例上重估截距：mean(expit(lp + a)) = mean(y)。"""
    obs = y.mean()
    lo, hi = -12.0, 12.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if expit(lp + mid).mean() < obs:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def resid_a(lp_eval, y_eval, a, b=1.0):
    """在评估集上算残余校准截距（把已应用的 a,b 折算掉）。"""
    return solve_a(lp_eval * b + a, y_eval)


MS = [0, 25, 50, 100, 200]
NREP = 100
R = None
_cache = os.path.join(ST, "learning_curve_raw.csv")
if "--nocache" not in sys.argv and os.path.exists(_cache):
    try:
        R = pd.read_csv(_cache)
        print(f"[cache] 读入 {_cache}（{len(R):,} 行）；如需重算请加 --nocache")
    except Exception:
        R = None
if R is None:
    recs = []
    groups = {h: (g["lp"].values, g["y"].values) for h, g in E.groupby("hospitalid")}
    print(f"[run] {len(groups)} 中心 × m∈{MS} × {NREP} 次重抽样")
    for h, (lp, y) in groups.items():
        n = len(lp)
        for m in MS:
            if m > 0 and n < 2 * m:
                continue
            if m == 0:
                a0 = solve_a(lp, y)
                oe0 = y.mean() / max(expit(lp).mean(), 1e-9)   # 不做任何校准 → 残余 O/E = 原始 O/E
                for strat in ["S1", "S2"]:
                    recs.append(dict(hospital=h, m=0, rep=0, strat=strat,
                                     resid_a=abs(a0), oe=oe0))
                continue
            for rep in range(NREP):
                idx = np.random.default_rng(20261019 + rep * 9973 + int(h)).choice(
                    n, size=m, replace=False)
                mask = np.ones(n, bool); mask[idx] = False
                lp_c, y_c = lp[idx], y[idx]
                lp_e, y_e = lp[mask], y[mask]
                if len(np.unique(y_c)) < 2 or len(np.unique(y_e)) < 2:
                    continue
                # S1 仅截距
                a1 = solve_a(lp_c, y_c)
                ra1 = abs(resid_a(lp_e, y_e, a1))
                oe1 = y_e.mean() / max(expit(lp_e + a1).mean(), 1e-9)
                recs.append(dict(hospital=h, m=m, rep=rep, strat="S1", resid_a=ra1, oe=oe1))
                # S2 截距 + 斜率
                mm = LogisticRegression(max_iter=5000, C=1e6).fit(
                    lp_c.reshape(-1, 1), y_c)
                b2 = float(mm.coef_[0, 0]); a2 = float(mm.intercept_[0])
                ra2 = abs(resid_a(lp_e, y_e, a2, b2))
                oe2 = y_e.mean() / max(expit(lp_e * b2 + a2).mean(), 1e-9)
                recs.append(dict(hospital=h, m=m, rep=rep, strat="S2", resid_a=ra2, oe=oe2))
    R = pd.DataFrame(recs)
    R.to_csv(_cache, index=False, encoding="utf-8-sig")
    print(f"[save] cache -> {_cache}")

R["oe_absdev"] = (R["oe"] - 1.0).abs()
R["ok11"] = (R["oe_absdev"] <= 0.10).astype(float)
R["ok12"] = (R["oe_absdev"] <= 0.20).astype(float)

print("\n" + "=" * 86)
print("### 本地重校准学习曲线（SOFA 模型；每 (h,m) 100 次重抽样）")
print("=" * 86)
print("  指标说明：residual |a| = 重抽样后残余校准截距的绝对值（每中心取 100 次的中位）；")
print("           达标率 = **每次重抽样**中 |O/E−1| ≤ 10%（或 20%）的比例，再对中心取平均")
print("           （不得用「残余 O/E 的中位数」判达标——重抽样误差无偏，中位数必然趋近 1）")
out = []
for strat in ["S1", "S2"]:
    print(f"\n-- {strat}  "
          f"{'仅重估截距' if strat=='S1' else '截距 + 校准斜率'} --")
    print(f"   {'m':>5} {'k(中心)':>8} {'残余|a| 中位':>12} {'P90':>8} "
          f"{'|O/E−1|≤10%':>13} {'|O/E−1|≤20%':>13}")
    for m in MS:
        g = R[(R["strat"] == strat) & (R["m"] == m)]
        if g.empty:
            continue
        per = g.groupby("hospital").agg(ra=("resid_a", "median"),
                                        oead=("oe_absdev", "median"),
                                        ok11=("ok11", "mean"), ok12=("ok12", "mean"))
        k = len(per)
        ra_med, ra_p90 = per["ra"].median(), np.percentile(per["ra"], 90)
        w11, w12 = 100 * per["ok11"].mean(), 100 * per["ok12"].mean()
        print(f"   {m:>5} {k:>8} {ra_med:>12.4f} {ra_p90:>8.4f} {w11:>12.1f}% {w12:>12.1f}%")
        out.append(dict(strat=strat, m=m, k=k, resid_a_med=round(ra_med, 4),
                        resid_a_p90=round(ra_p90, 4), oe_absdev_med=round(float(per["oead"].median()), 4),
                        within_09_11=round(w11, 1), within_08_12=round(w12, 1)))
json.dump(out, open(os.path.join(ST, "learning_curve_summary.json"), "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("[saved] learning_curve_summary.json")
print("[done]")
