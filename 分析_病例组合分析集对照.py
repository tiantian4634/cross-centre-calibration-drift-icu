# -*- coding: utf-8 -*-
"""A5 参照计算（严格口径）：
在 M3 的患者子集、M3 的中心集合上，只把模型换回 M1（SOFA 单评分），
看 I² 是否仍接近全队列 M1 的 75.4%。若接近，则 M3 的下降可归因于协变量本身。

复现顺序与 analysis_drift.py 一致：先在相应子集上拟合合并模型，再逐院求 a_h，
最后只对满足 n≥100 且死亡≥10 的中心做 DerSimonian–Laird。
"""
import io, sys, os, json
import numpy as np, pandas as pd
from scipy.special import expit, logit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST = os.path.join(B, "03_统计")
sys.path.insert(0, B)
from figures_common import r1

hid = pd.read_csv(os.path.join(B, "hospital_id_map.csv"), usecols=["stay_id", "hospitalid"])
E = pd.read_csv(os.path.join(os.path.dirname(B), "02_数据集", "cohort_eicu.csv"), low_memory=False)
E = E.merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int)


def solve_a(lp, y):
    obs = y.mean(); lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if expit(lp + mid).mean() < obs: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def dersimonian(a, se):
    w = 1.0 / se ** 2
    ab = np.sum(w * a) / np.sum(w)
    Q = np.sum(w * (a - ab) ** 2)
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (len(a) - 1)) / C)
    I2 = (Q - (len(a) - 1)) / Q * 100 if Q > 0 else 0.0
    return tau2, I2


def run(d, cols, label):
    """拟合合并模型 → 逐院 a_h → 仅对 n≥100 且死亡≥10 的中心做 meta"""
    d = d.dropna(subset=cols + ["y"]).copy()
    X = d[cols].astype(float).values
    mu, sd = X.mean(0), np.where(X.std(0) == 0, 1, X.std(0))
    m = LogisticRegression(max_iter=5000, C=1.0).fit((X - mu) / sd, d["y"].values)
    d["p"] = m.predict_proba((X - mu) / sd)[:, 1]
    d["lp"] = logit(np.clip(d["p"].values, 1e-8, 1 - 1e-8))
    auc = roc_auc_score(d["y"], d["p"])
    rows = []
    for h, g in d.groupby("hospitalid"):
        if len(g) < 100 or int(g["y"].sum()) < 10:
            continue
        a = solve_a(g["lp"].values, g["y"].values)
        pp = expit(g["lp"].values + a)
        se = np.sqrt(max(g["y"].mean() * (1 - g["y"].mean()), 1e-9) / len(g)) \
             / max(float(np.mean(pp * (1 - pp))), 1e-9)
        rows.append((h, a, se))
    a = np.array([r[1] for r in rows]); se = np.array([r[2] for r in rows])
    tau2, I2 = dersimonian(a, se)
    print("  %-44s n=%-7d k=%-4d AUC=%.4f  I²=%.2f%%  τ²=%.4f"
          % (label, len(d), len(rows), auc, I2, tau2))
    return dict(n=int(len(d)), k=int(len(rows)), auc=round(float(auc), 4),
                I2=round(float(I2), 4), tau2=round(float(tau2), 4))


SOFA = ["sofa"]
FULL = ["sofa", "age", "male", "cci", "invasive_vent"]

print("=" * 92)
print("  A5 参照计算（严格口径）")
print("=" * 92)
print("\n  —— 复现验证（须与 drift_results.json 一致）——")
a1 = run(E, SOFA, "M1  全队列")
print("      权威 M1: k=103, AUC=0.7318, I²=75.35, τ²=0.1312")
ok1 = abs(a1["I2"] - 75.35) < 0.3 and a1["k"] == 103
print("      复现: %s" % ("✔ 一致" if ok1 else "✘ 不一致，勿用"))

d3 = E.dropna(subset=["cci", "invasive_vent"]).copy()
print("\n  —— 关键参照 ——")
m3 = run(d3, FULL, "M3  加协变量（n=27,236 子集）")
print("      权威 M3: k=97, I²=70.12, τ²=0.1055")
ok3 = m3["k"] == 97 and abs(m3["I2"] - 70.12) < 0.5
print("      复现: %s" % ("✔ 一致" if ok3 else "✘ 不一致，勿用"))

m1_same = run(d3, SOFA, "M1  在 M3 的同一患者子集上")
# 同一患者子集 + 同一中心集合（m3 的 k 家中心）→ 再算一次 I² 以对齐中心集合
X = d3[SOFA].astype(float).values
mu, sd = X.mean(0), X.std(0)
mm = LogisticRegression(max_iter=5000, C=1.0).fit((X - mu) / sd, d3["y"].values)
d3 = d3.copy()
d3["p"] = mm.predict_proba((X - mu) / sd)[:, 1]
d3["lp"] = logit(np.clip(d3["p"].values, 1e-8, 1 - 1e-8))
keep3 = []
for h, g in d3.groupby("hospitalid"):
    if len(g) >= 100 and int(g["y"].sum()) >= 10:
        aa = solve_a(g["lp"].values, g["y"].values)
        pp = expit(g["lp"].values + aa)
        s = np.sqrt(max(g["y"].mean() * (1 - g["y"].mean()), 1e-9) / len(g)) / max(float(np.mean(pp * (1 - pp))), 1e-9)
        keep3.append((aa, s))
keep3 = np.array(keep3)
t2, i2 = dersimonian(keep3[:, 0], keep3[:, 1])
print("  M1  同患者子集 + 同 %d 家中心          I²=%.2f%%  τ²=%.4f" % (len(keep3), i2, t2))

print("\n" + "=" * 92)
print("  判读")
print("=" * 92)
print("  M1（全队列，103 中心）            I² = %.2f%%   ← 起点 75.4%%" % a1["I2"])
print("  M3（加协变量，97 中心）           I² = %.2f%%   ← 终点 70.1%%" % m3["I2"])
print("  M1（M3 的患者子集与中心集合）      I² = %.2f%%   ← 参照柱" % i2)
d_set = i2 - a1["I2"]
d_cov = m3["I2"] - i2
print("\n  总下降           %.2f 个百分点（75.35 → 70.12）" % (m3["I2"] - a1["I2"]))
print("  分析集变化贡献   %+.2f 个百分点" % d_set)
print("  协变量本身贡献   %+.2f 个百分点" % d_cov)
if abs(d_set) < abs(d_cov):
    print("\n  ✔ 协变量解释的部分大于分析集变化 —— 参照柱可安全加入 SuppFig S1，")
    print("     并在正文写明「the reduction is attributable to the covariates rather than to the")
    print("     change in analysis set」。")
else:
    print("\n  ⚠ 分析集变化贡献 %.1f 个百分点，超过协变量 —— 正文须如实说明。" % abs(d_set))

json.dump(dict(m1_full=a1, m3=m3, m1_same_subset_k=int(len(keep3)),
               I2_m1_same_subset=round(float(i2), 4),
               delta_set_pp=round(float(d_set), 4), delta_cov_pp=round(float(d_cov), 4)),
          open(os.path.join(ST, "casemix_set_sensitivity.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("\n  -> 03_统计\\casemix_set_sensitivity.json")
print("=" * 92)