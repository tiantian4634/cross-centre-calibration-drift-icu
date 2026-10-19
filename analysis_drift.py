# -*- coding: utf-8 -*-
"""
路B 主分析 · 严重度评分的跨中心可迁移性（判别 vs 校准）
========================================
只读本地 cohort CSV + hospitalid 映射；不连库、不改既有正式文件。

【预注册】先写下分析计划（写入 03_统计\\分析计划_预注册.md）：

  A 逐院校准漂移：CITL 截距 a_h（斜率固定 1）+ 校准斜率 b_h（截距自由）
  B 三种严重度评分对比：SOFA / OASIS / SAPS-II 的 I²、tau²、O/E 范围、AUC 范围
  C 病例组合阶梯：I² 是否随协变量增多而明显下降？
       M1 = score
       M2 = score + age + sex
       M3 = score + age + sex + cci + invasive_vent
     → 若 I² 在 M3 仍高，说明漂移不是"病情轻重"能解释的
        （但**不得**因此解读为医疗质量差异，只能称"残余漂移"）
  D MIMIC 单中心在 eICU 分布中的位置（外部对照）

  判据（事前）：I² > 50% 且 n≥100 医院 ≥ 100 家 → 成立（已在探测轮确认）
"""
import io, sys, os, json, datetime
import numpy as np, pandas as pd
from scipy.special import expit, logit
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
SRCDIR = os.path.join(BASE, "09_路B_跨院校准")
OUT = os.path.join(SRCDIR, "03_统计"); FIG = os.path.join(SRCDIR, "04_图表")
os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

PRE = """# 路B 主分析 · 预注册分析计划
生成：{ts}（先于结果）

| 编号 | 分析 | 产出 |
|---|---|---|
| A | 逐院校准：CITL 截距 a_h（斜率固定1）+ 校准斜率 b_h（截距自由） | 逐院表 + caterpillar |
| B | 三评分对比 SOFA / OASIS / SAPS-II | 异质性对照表 + 三联图 |
| C | 病例组合阶梯 M1=score / M2=+age+sex / M3=+cci+vent | I² 阶梯表 |
| D | MIMIC 单中心在 eICU 分布中的位置 | 定位表 |

**措辞红线（预注册）**：C 中未被病例组合解释的漂移一律称 **"residual between-hospital variation / 残余院间变异"**，
**不得**表述为"医疗质量差异"或"医院水平高低"——未测量的病例组合、转诊模式、社会经济均可致残余变异。

## 分析集
逐院分析阈值：**n ≥ 100 且院内死亡 ≥ 10**（0 事件医院会使校准截距不可估）。
三种评分各自在其非缺失子集上拟合，以保证可比；同时报告各评分的缺失率。
"""
_prereg_path = os.path.join(OUT, "分析计划_预注册.md")
if not os.path.exists(_prereg_path):      # 幂等：已存在则不覆盖，以保住原始写入时间戳
    open(_prereg_path, "w", encoding="utf-8").write(PRE.replace("{ts}", ts))
    print("[pre-reg] 分析计划已写入")
else:
    print("[pre-reg] 分析计划_预注册.md 已存在，保留原始时间戳，不覆盖")

# ---------------- 数据 ----------------
hid = pd.read_csv(os.path.join(SRCDIR, "hospital_id_map.csv")) if os.path.exists(
    os.path.join(SRCDIR, "hospital_id_map.csv")) else None
if hid is None:
    import duckdb
    con = duckdb.connect(r"F:\数据库\MIMIC\mimic-SQL知识库\catalog.duckdb", read_only=True)
    hid = con.execute('select patientunitstayid as stay_id, hospitalid '
                      'from "eicu_crd.eicu_crd".patient').fetchdf()
    con.close()
    hid.to_csv(os.path.join(SRCDIR, "hospital_id_map.csv"), index=False)

E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv")).merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid"]).copy()
M = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_mimiciv.csv"))
E["y"] = E["hosp_death"].astype(int); M["y"] = M["hosp_death"].astype(int)
print(f"[data] eICU {len(E):,} 例 / {E['hospitalid'].nunique()} 家医院；MIMIC {len(M):,} 例（单中心）")
print(f"[missing] eICU 各评分缺失率："
      f"SOFA {100*E['sofa'].isna().mean():.1f}%  OASIS {100*E['oasis'].isna().mean():.1f}%  "
      f"SAPS-II {100*E['sapsii'].isna().mean():.1f}%")

SCORES = [("SOFA", "sofa"), ("OASIS", "oasis"), ("SAPS-II", "sapsii")]
MIN_N, MIN_D = 100, 10


def pooled(df, cols):
    d = df.dropna(subset=cols + ["y"]).copy()
    X = d[cols].astype(float).values
    mu, sd = X.mean(0), np.where(X.std(0) == 0, 1, X.std(0))
    Xs = (X - mu) / sd
    m = LogisticRegression(max_iter=5000, C=1.0).fit(Xs, d["y"].values)
    d["p"] = m.predict_proba(Xs)[:, 1]
    return d, m, roc_auc_score(d["y"], d["p"])


def calib_int(p, obs):
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if expit(logit(np.clip(p, 1e-8, 1 - 1e-8)) + mid).mean() < obs:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def per_hosp(d, min_n=MIN_N, min_d=MIN_D):
    rows = []
    lp = logit(np.clip(d["p"].values, 1e-8, 1 - 1e-8)).reshape(-1, 1)
    for h, g in d.groupby("hospitalid"):
        n = len(g); dd = int(g["y"].sum())
        if n < min_n or dd < min_d:
            continue
        obs = dd / n
        a = calib_int(g["p"].values, obs)
        pp = expit(logit(np.clip(g["p"].values, 1e-8, 1 - 1e-8)) + a)
        se_a = np.sqrt(max(obs * (1 - obs), 1e-9) / n) / max(float(np.mean(pp * (1 - pp))), 1e-9)
        lg = logit(np.clip(g["p"].values, 1e-8, 1 - 1e-8)).reshape(-1, 1)
        mm = LogisticRegression(max_iter=5000, C=1e6).fit(lg, g["y"].values)   # 近似无惩罚
        rows.append(dict(hospital=h, n=n, deaths=dd, obs=obs, exp=g["p"].mean(),
                         OE=obs / max(g["p"].mean(), 1e-9), a_h=a, se_a=se_a,
                         b_h=float(mm.coef_[0, 0]), auc=roc_auc_score(g["y"], g["p"]),
                         score_mean=float(g.iloc[:, 0].mean()) if False else np.nan))
    return pd.DataFrame(rows)


def dersimonian(a, se):
    a, se = np.asarray(a, float), np.asarray(se, float)
    w = 1.0 / se ** 2
    abar = np.sum(w * a) / np.sum(w)
    Q = np.sum(w * (a - abar) ** 2)
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (len(a) - 1)) / C)
    I2 = max(0.0, (Q - (len(a) - 1)) / Q) * 100 if Q > 0 else 0.0
    seRE = np.sqrt(1.0 / np.sum(1.0 / (se ** 2 + tau2)))
    return abar, tau2, I2, Q, seRE


RES, HOSP = {}, {}
print("\n" + "=" * 84)
print("### A+B  逐院漂移 + 三评分对比（阈值 n≥%d 且事件≥%d）" % (MIN_N, MIN_D))
print("=" * 84)
for name, col in SCORES:
    d, m, auc = pooled(E, [col])
    H = per_hosp(d)
    abar, tau2, I2, Q, seRE = dersimonian(H["a_h"], H["se_a"])
    H["score"] = name
    HOSP[name] = H
    RES[name] = dict(pooled_n=len(d), pooled_events=int(d["y"].sum()), pooled_auc=round(auc, 4),
                     k=len(H), I2=round(I2, 2), tau2=round(tau2, 4),
                     a_bar=round(abar, 4), seRE=round(seRE, 4),
                     OE_p10=round(float(np.percentile(H["OE"], 10)), 3),
                     OE_med=round(float(H["OE"].median()), 3),
                     OE_p90=round(float(np.percentile(H["OE"], 90)), 3),
                     auc_p10=round(float(np.percentile(H["auc"], 10)), 3),
                     auc_med=round(float(H["auc"].median()), 3),
                     auc_p90=round(float(np.percentile(H["auc"], 90)), 3),
                     bh_p10=round(float(np.percentile(H["b_h"], 10)), 3),
                     bh_med=round(float(H["b_h"].median()), 3),
                     bh_p90=round(float(np.percentile(H["b_h"], 90)), 3))
    print(f"\n-- {name}（pooled AUC {auc:.4f}；逐院 k={len(H)}）--")
    print(f"   I² = {I2:6.2f}%   tau² = {tau2:.4f}   合并 a = {abar:+.4f}")
    print(f"   O/E    P10 {np.percentile(H['OE'],10):.2f}  中位 {H['OE'].median():.2f}  P90 {np.percentile(H['OE'],90):.2f}")
    print(f"   AUC    P10 {np.percentile(H['auc'],10):.3f}  中位 {H['auc'].median():.3f}  P90 {np.percentile(H['auc'],90):.3f}")
    print(f"   校准斜率 b_h  P10 {np.percentile(H['b_h'],10):.3f}  中位 {H['b_h'].median():.3f}  P90 {np.percentile(H['b_h'],90):.3f}")

# ---------------- C 病例组合阶梯（SOFA） ----------------
print("\n" + "=" * 84)
print("### C  痂例组合阶梯：I² 是否随协变量增多而下降（评分 = SOFA）")
print("=" * 84)
LADDER = {}
for tag, cols in [("M1  SOFA", ["sofa"]),
                  ("M2  SOFA + age + sex", ["sofa", "age", "male"]),
                  ("M3  + cci + invasive_vent", ["sofa", "age", "male", "cci", "invasive_vent"])]:
    d, m, auc = pooled(E, cols)
    d = d.dropna(subset=["cci", "invasive_vent"]) if "cci" in cols else d
    d, m, auc = pooled(d, cols)
    H = per_hosp(d)
    abar, tau2, I2, Q, seRE = dersimonian(H["a_h"], H["se_a"])
    LADDER[tag] = dict(k=len(H), AUC=round(auc, 4), I2=round(I2, 2), tau2=round(tau2, 4),
                       OE_p10=round(float(np.percentile(H["OE"], 10)), 3),
                       OE_p90=round(float(np.percentile(H["OE"], 90)), 3))
    print(f"   {tag:<28} k={len(H):>4}  AUC {auc:.4f}  **I² {I2:5.2f}%**  tau² {tau2:.4f}  "
          f"O/E P10-P90 {np.percentile(H['OE'],10):.2f}–{np.percentile(H['OE'],90):.2f}")

# ---------------- D MIMIC 定位 ----------------
print("\n" + "=" * 84)
print("### D  MIMIC 单中心在 eICU 分布中的位置（SOFA 模型）")
print("=" * 84)
dE, mE, aucE = pooled(E, ["sofa"])
dM = M.dropna(subset=["sofa"]).copy()
X = dM[["sofa"]].values
# 用 eICU 的标准化参数投影
mu = dE["sofa"].mean(); sd = dE["sofa"].std()
dM["p"] = mE.predict_proba(((X - mu) / sd))[:, 1]
obsM = dM["y"].mean()
aM = calib_int(dM["p"].values, obsM)
aucM = roc_auc_score(dM["y"], dM["p"])
H = HOSP["SOFA"]
pct = float((H["a_h"] < aM).mean() * 100)
print(f"   eICU 合并模型 → MIMIC：AUC {aucM:.4f}（eICU 内 {aucE:.4f}）")
print(f"   MIMIC 观测死亡率 {100*obsM:.1f}%  预测均值 {100*dM['p'].mean():.1f}%  "
      f"O/E {obsM/dM['p'].mean():.2f}")
print(f"   **MIMIC 校准截距 a = {aM:+.4f}，位于 eICU {len(H)} 家医院分布的第 {pct:.0f} 百分位**")
MIM = dict(auc_mimic=round(aucM, 4), auc_eicu=round(aucE, 4), obs=round(float(obsM), 4),
           exp=round(float(dM["p"].mean()), 4), OE=round(float(obsM / dM["p"].mean()), 3),
           a=round(float(aM), 4), percentile=round(pct, 1))

# ---------------- 存盘 ----------------
pd.concat(HOSP.values()).to_csv(os.path.join(OUT, "hospital_level_三评分.csv"), index=False, encoding="utf-8-sig")
json.dump(dict(scores=RES, ladder=LADDER, mimic=MIM), open(
    os.path.join(OUT, "drift_results.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("\n[out] hospital_level_三评分.csv / drift_results.json ->", OUT)
