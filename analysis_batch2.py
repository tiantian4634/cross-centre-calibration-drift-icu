# -*- coding: utf-8 -*-
"""
路B 第二批分析：F 时间稳定性(split-half) / G 医院规模分层 / H 临床影响
========================================
【预注册】先写下设计（写入 03_统计\\分析计划_第二批.md）：

  F  时间稳定性（split-half）
     eICU 仅覆盖 2014–2015；167 家医院两年都有数据。
     对每家医院分别算 2014 与 2015 的校准截距 a_h，考察：
       (a) 两年 a_h 的相关性（split-half reliability）
       (b) 同一医院两年的 |Δa|
       (c) 同一医院两年内变异 vs 医院间变异
     若相关性低 → 「医院身份」并不稳定，部分院间差异是不稳定的，而非固定属性。
     纳入：每年 n ≥ 50 且院内死亡 ≥ 5。

  G  医院规模分层
     按每院 n 的三分位分层，比较各层的 I²、tau²、O/E 跨度。
     假设：小样本中心的表观漂移更大（噪声更多）。

  H  临床影响
     在决策阈值 pt ∈ {0.10, 0.20, 0.30, 0.40} 下，逐院计算净获益
       NB = TP/n − FP/n × pt/(1−pt)
     以及"被判为高风险者中的实际病死率"（PPV）。
     回答：同一个阈值在不同医院意味着什么？

  措辞红线：F 的低相关只说明"表观院间变异含不稳定成分"，
            不得解读为"医院质量不稳定"。
"""
import io, sys, os, json, datetime
import numpy as np, pandas as pd
from scipy.special import expit, logit
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def _write_prereg(path, text):
    """幂等写入预注册文档：已存在则不覆盖，以保住『先于结果』的原始时间戳。"""
    if os.path.exists(path):
        print(f"[pre-reg] {os.path.basename(path)} 已存在，保留原始时间戳，不覆盖")
    else:
        open(path, "w", encoding="utf-8").write(text)
        print(f"[pre-reg] 已写入 {os.path.basename(path)}")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
SRCDIR = os.path.join(BASE, "09_路B_跨院校准")
ST, FG = os.path.join(SRCDIR, "03_统计"), os.path.join(SRCDIR, "04_图表")
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

PRE = """# 路B 第二批分析 · 预注册
生成：{ts}（先于结果）

| 编号 | 分析 | 纳入 | 核心指标 |
|---|---|---|---|
| F | 时间稳定性 split-half（2014 vs 2015） | 每年 n≥50 且死亡≥5 | 两年 a_h 的 Pearson/Spearman 相关；\\|Δa\\| 中位；院内 vs 院间方差 |
| G | 医院规模分层（每院 n 三分位） | 全部可算中心 | 各层 I²、tau²、O/E P10–P90 |
| H | 临床影响（决策阈值 pt=0.10/0.20/0.30/0.40） | 全部可算中心 | 逐院净获益 NB = TP/n − FP/n·pt/(1−pt)；PPV |

**措辞红线**：F 的低相关只说明「表观院间变异含不稳定成分」，不得解读为「医院质量不稳定」。
"""
_write_prereg(os.path.join(ST, "分析计划_第二批.md"), PRE.replace("{ts}", ts))
print("[pre-reg] 已写入 分析计划_第二批.md")

# ---------------- 数据 ----------------
ctx = pd.read_csv(os.path.join(SRCDIR, "eicu_hospital_context.csv"))
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv")).merge(
    ctx[["stay_id", "hospitalid", "hospitaldischargeyear", "unittype"]], on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int); E["yr"] = E["hospitaldischargeyear"].astype(int)
mu, sd = E["sofa"].mean(), E["sofa"].std()
m = LogisticRegression(max_iter=5000, C=1.0).fit(((E[["sofa"]].values - mu) / sd), E["y"].values)
E["p"] = m.predict_proba((E[["sofa"]].values - mu) / sd)[:, 1]
print(f"[data] {len(E):,} 例；合并 AUC {roc_auc_score(E['y'], E['p']):.4f}")


def solve_a(p, obs, lo=-12.0, hi=12.0):
    lp = logit(np.clip(np.asarray(p, float), 1e-8, 1 - 1e-8))
    for _ in range(120):
        mid = (lo + hi) / 2
        if expit(lp + mid).mean() < obs:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def dersimonian(a, se):
    a, se = np.asarray(a, float), np.asarray(se, float)
    w = 1.0 / se ** 2
    abar = np.sum(w * a) / np.sum(w)
    Q = np.sum(w * (a - abar) ** 2)
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (len(a) - 1)) / C)
    I2 = max(0.0, (Q - (len(a) - 1)) / Q) * 100 if Q > 0 else 0.0
    return abar, tau2, I2


# ══════════════ F  时间稳定性 ══════════════
print("\n" + "=" * 80)
print("### F  时间稳定性（split-half：2014 vs 2015）")
print("=" * 80)
rows = []
for h, g in E.groupby("hospitalid"):
    a = {}
    for yr in (2014, 2015):
        s = g[g["yr"] == yr]
        if len(s) < 50 or s["y"].sum() < 5:
            a = None; break
        obs = s["y"].mean()
        av = solve_a(s["p"].values, obs)
        pp = expit(logit(np.clip(s["p"].values, 1e-8, 1 - 1e-8)) + av)
        se = np.sqrt(max(obs * (1 - obs), 1e-9) / len(s)) / max(float(np.mean(pp * (1 - pp))), 1e-9)
        a[yr] = (av, se, len(s), int(s["y"].sum()))
    if a:
        rows.append(dict(hospital=h, a14=a[2014][0], se14=a[2014][1], n14=a[2014][2], d14=a[2014][3],
                         a15=a[2015][0], se15=a[2015][1], n15=a[2015][2], d15=a[2015][3]))
F = pd.DataFrame(rows)
F["da"] = F["a15"] - F["a14"]
F.to_csv(os.path.join(ST, "temporal_split_half.csv"), index=False, encoding="utf-8-sig")
r_p, pr = pearsonr(F["a14"], F["a15"])
r_s, ps = spearmanr(F["a14"], F["a15"])
_, tau_b, I2_b = dersimonian(np.r_[F["a14"], F["a15"]],
                             np.r_[F["se14"], F["se15"]])
var_within = float(np.var(F["da"], ddof=1) / 2)
var_between = float(np.var(np.r_[F["a14"], F["a15"]], ddof=1))
print(f"  纳入中心 k = {len(F)}（每年 n≥50 且死亡≥5）")
print(f"  两年 a_h 相关：Pearson r = **{r_p:+.3f}** (P={pr:.3g})；Spearman ρ = {r_s:+.3f} (P={ps:.3g})")
print(f"  同一医院两年 |Δa| 中位 = {np.median(np.abs(F['da'])):.4f}（P90 = {np.percentile(np.abs(F['da']),90):.4f}）")
print(f"  院内（时间）方差 ≈ {var_within:.4f}；院间总方差 ≈ {var_between:.4f} → "
      f"**时间成分占 {100*var_within/var_between:.1f}%**")
print(f"  2014→2015 平均漂移 a = {F['da'].mean():+.4f}（t={F['da'].mean()/(F['da'].std(ddof=1)/np.sqrt(len(F))):.2f}）")

# ══════════════ G  医院规模分层 ══════════════
print("\n" + "=" * 80)
print("### G  医院规模分层（每院 n 三分位）")
print("=" * 80)
H = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
H = H[H["score"] == "SOFA"].copy()
H["size"] = pd.qcut(H["n"], 3, labels=["小", "中", "大"])
GL = {}
for lab, g in H.groupby("size", observed=True):
    _, tau2, I2 = dersimonian(g["a_h"], g["se_a"])
    GL[str(lab)] = dict(k=len(g), n_med=float(g["n"].median()), n_min=int(g["n"].min()),
                        n_max=int(g["n"].max()), I2=round(I2, 2), tau2=round(tau2, 4),
                        OE_p10=round(float(np.percentile(g["OE"], 10)), 3),
                        OE_p90=round(float(np.percentile(g["OE"], 90)), 3),
                        auc_med=round(float(g["auc"].median()), 3))
    print(f"  {lab}中心：k={len(g):>4}  每院 n 中位 {g['n'].median():>6.0f} ({int(g['n'].min())}–{int(g['n'].max())})  "
          f"I² {I2:5.2f}%  tau² {tau2:.4f}  O/E P10–P90 {np.percentile(g['OE'],10):.2f}–{np.percentile(g['OE'],90):.2f}")

# ══════════════ H  临床影响 ══════════════
print("\n" + "=" * 80)
print("### H  临床影响：同一个决策阈值在不同医院意味着什么")
print("=" * 80)
THR = [0.10, 0.20, 0.30, 0.40]
HL = []
for pt in THR:
    rec = []
    for h, g in E.groupby("hospitalid"):
        if len(g) < 100:
            continue
        flag = (g["p"].values >= pt)
        n = len(g); tp = int((flag & (g["y"].values == 1)).sum()); fp = int((flag & (g["y"].values == 0)).sum())
        nb = tp / n - fp / n * (pt / (1 - pt))
        ppv = tp / max(tp + fp, 1)
        rec.append(dict(hospital=h, n=n, flagged_pct=100 * flag.mean(), ppv=100 * ppv, nb=nb))
    d = pd.DataFrame(rec)
    HL.append(dict(pt=pt, k=len(d),
                   flag_med=float(d["flagged_pct"].median()),
                   flag_p10=float(np.percentile(d["flagged_pct"], 10)),
                   flag_p90=float(np.percentile(d["flagged_pct"], 90)),
                   ppv_med=float(d["ppv"].median()),
                   ppv_p10=float(np.percentile(d["ppv"], 10)),
                   ppv_p90=float(np.percentile(d["ppv"], 90)),
                   nb_med=float(d["nb"].median()),
                   nb_p10=float(np.percentile(d["nb"], 10)),
                   nb_p90=float(np.percentile(d["nb"], 90)),
                   nb_neg_pct=float(100 * (d["nb"] < 0).mean())))
    print(f"  pt={pt:.2f}｜k={len(d)}｜被判高风险比例中位 {d['flagged_pct'].median():.1f}% ｜"
          f"其中实际死亡率(PPV) 中位 {d['ppv'].median():.1f}% (P10–P90 {np.percentile(d['ppv'],10):.1f}–{np.percentile(d['ppv'],90):.1f}%)｜"
          f"净获益中位 {d['nb'].median():+.4f} (P10–P90 {np.percentile(d['nb'],10):+.4f}–{np.percentile(d['nb'],90):+.4f})｜"
          f"**净获益为负的医院 {d['nb'].lt(0).mean()*100:.1f}%**")
json.dump(dict(F=dict(k=len(F), r=round(r_p, 3), p=pr, rho=round(r_s, 3),
                      da_med=round(float(np.median(np.abs(F["da"]))), 4),
                      var_within=round(var_within, 4), var_between=round(var_between, 4),
                      temporal_share_pct=round(100 * var_within / var_between, 1),
                      da_mean=round(float(F["da"].mean()), 4)),
                 G=GL, H=HL),
          open(os.path.join(ST, "batch2_results.json"), "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("\n[out] temporal_split_half.csv / batch2_results.json ->", ST)
