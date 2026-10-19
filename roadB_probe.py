# -*- coding: utf-8 -*-
"""
路B 可行性探测 · eICU 跨院校准漂移（只读 DuckDB；产物独立于 09_路B_跨院校准\\）

【预注册】先写下要回答的问题与判据（写入 路B_预注册.md）：

  Q1 eICU 中可用于"逐院分析"的医院有多少？（阈值 n≥50 / n≥100）
  Q2 同一个 SOFA/严重度模型，在不同医院的**校准截距**漂移有多大？
     → 用随机效应 meta 分析（DerSimonian-Laird）估计院间方差 tau² 与 I²。
  Q3 这种漂移有多少来自**病例组合**差异（各院病情轻重不同），有多少是**残余**？
     → 医院平均 SOFA 与院死亡率的 Spearman 相关。
  Q4 逐院判别力（SOFA 单独的 AUC）分布如何？→ 若院间稳定而校准漂移大，
     则"判别可迁移、校准不可迁移"是论文核心结论。

  判据：若 I² > 50% 且 n≥100 的医院 ≥ 100 家 → 路B 成立（信号强、样本足）。
"""
import io, sys, os, json, datetime
import numpy as np, pandas as pd, duckdb
from scipy.special import expit, logit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
OUT = os.path.join(BASE, "09_路B_跨院校准")
os.makedirs(OUT, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

PREREG = """# 路B 可行性探测 · 预注册
生成：{ts}（**先于结果写下**）

## 要回答的问题
- **Q1** 可用于逐院分析的医院数（阈值 n≥50 / n≥100）
- **Q2** 院间校准截距漂移：随机效应 meta 分析（DerSimonian-Laird）→ tau² 与 I²
- **Q3** 漂移有多少来自病例组合：医院平均 SOFA vs 院死亡率的 Spearman 相关
- **Q4** 逐院判别力分布（SOFA 单独 AUC）

## 模型
Pooled logistic：death ~ SOFA + age + sex（eICU 全队列标准化拟合）
每院的**校准截距 a_h**：解 mean(expit(logit(p̂) + a_h)) = 院实测死亡率
（a_h = 0 表示该院与总体校准一致；a_h>0 表示该院死亡率高于模型预期）

## 判据（事前设定）
**I² > 50% 且 n≥100 的医院 ≥ 100 家 → 路B 成立**（信号强 + 样本足）。
"""
open(os.path.join(OUT, "路B_预注册.md"), "w", encoding="utf-8").write(PREREG.replace("{ts}", ts))
print("[pre-reg] 已写入 路B_预注册.md")

# ---------- 1. 取 hospitalid（只读） ----------
con = duckdb.connect(r"F:\数据库\MIMIC\mimic-SQL知识库\catalog.duckdb", read_only=True)
hid = con.execute('select patientunitstayid as stay_id, hospitalid, unittype, uniquepid '
                  'from "eicu_crd.eicu_crd".patient').fetchdf()
con.close()
print(f"[db] eICU hospitalid 映射 {len(hid):,} 行")

df = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv"))
n0 = len(df)
df = df.merge(hid, on="stay_id", how="left")
print(f"[join] 队列 {n0:,} 例 → 取到 hospitalid {df['hospitalid'].notna().sum():,} 例")
df = df.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
df["sofa"] = df["sofa"].astype(float); df["age"] = df["age"].astype(float)
df["male"] = df["male"].astype(float); df["y"] = df["hosp_death"].astype(int)
print(f"[clean] 分析集 n={len(df):,}，事件 {df['y'].sum():,}（{100*df['y'].mean():.2f}%），"
      f"医院 {df['hospitalid'].nunique()} 家")

# ---------- 2. Pooled 模型 ----------
X = df[["sofa", "age", "male"]].values
Xs = (X - X.mean(0)) / X.std(0)
m = LogisticRegression(max_iter=3000, C=1.0).fit(Xs, df["y"].values)
df["p"] = m.predict_proba(Xs)[:, 1]
print(f"[pooled] AUC={roc_auc_score(df['y'], df['p']):.4f}  "
      f"β_SOFA={m.coef_[0,0]:.4f}  β_age={m.coef_[0,1]:.4f}  β_sex={m.coef_[0,2]:.4f}  "
      f"intercept={m.intercept_[0]:.4f}")

# SOFA 单独模型（供逐院 AUC）
X1 = df[["sofa"]].values; X1s = (X1 - X1.mean(0)) / X1.std(0)
m1 = LogisticRegression(max_iter=3000, C=1.0).fit(X1s, df["y"].values)
df["p_sofa"] = m1.predict_proba(X1s)[:, 1]
print(f"[pooled·SOFA单独] AUC={roc_auc_score(df['y'], df['p_sofa']):.4f}")

# ---------- 3. 逐院校准截距 ----------
def calib_intercept(p, obs):
    """解 mean(expit(logit(p)+a)) = obs，二分法。"""
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if expit(logit(np.clip(p, 1e-8, 1 - 1e-8)) + mid).mean() < obs:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

rows = []
for h, g in df.groupby("hospitalid"):
    n = len(g); d = int(g["y"].sum()); obs = d / n
    a = calib_intercept(g["p"].values, obs)
    # SE：delta 法，SE(a) ≈ sqrt(obs(1-obs)/n) / mean(d expit)
    pp = expit(logit(np.clip(g["p"].values, 1e-8, 1 - 1e-8)) + a)
    slope = float(np.mean(pp * (1 - pp)))
    se = np.sqrt(max(obs * (1 - obs), 1e-9) / n) / max(slope, 1e-9)
    auc = roc_auc_score(g["y"], g["p_sofa"]) if g["y"].nunique() == 2 and n >= 20 else np.nan
    rows.append(dict(hospital=h, n=n, deaths=d, obs=obs, exp=g["p"].mean(),
                     OE=obs / max(g["p"].mean(), 1e-9), a_h=a, se_a=se,
                     auc_sofa=auc, sofa_mean=g["sofa"].mean(), sofa_sd=g["sofa"].std()))
H = pd.DataFrame(rows).sort_values("a_h").reset_index(drop=True)
H.to_csv(os.path.join(OUT, "hospital_level.csv"), index=False, encoding="utf-8-sig")

# ---------- 4. 随机效应 meta 分析（DerSimonian-Laird） ----------
def dersimonian(a, se):
    w = 1.0 / se ** 2
    abar = np.sum(w * a) / np.sum(w)
    Q = np.sum(w * (a - abar) ** 2)
    C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (len(a) - 1)) / C)
    I2 = max(0.0, (Q - (len(a) - 1)) / Q) * 100 if Q > 0 else 0.0
    seRE = np.sqrt(1.0 / (np.sum(1.0 / (se ** 2 + tau2))))
    return abar, tau2, I2, Q, seRE

print("\n" + "=" * 78)
print("### Q1 可用于逐院分析的医院数")
print("=" * 78)
for th in [10, 20, 30, 50, 100, 200]:
    sub = H[H["n"] >= th]
    print(f"  n≥{th:>3}：{len(sub):>4} 家医院，覆盖 {int(sub['n'].sum()):>7,} 例"
          f"（{100*sub['n'].sum()/len(df):5.1f}% 的队列）")

for th in [50, 100]:
    sub = H[H["n"] >= th].dropna(subset=["a_h", "se_a"])
    abar, tau2, I2, Q, seRE = dersimonian(sub["a_h"].values, sub["se_a"].values)
    print("\n" + "=" * 78)
    print(f"### Q2/Q3/Q4 · 阈值 n≥{th}（{len(sub)} 家医院）")
    print("=" * 78)
    print(f"  随机效应合并校准截距   a = {abar:+.4f} (95%CI {abar-1.96*seRE:+.4f} ~ {abar+1.96*seRE:+.4f})")
    print(f"  院间方差 tau²           = {tau2:.4f}   → 院间 SD = {np.sqrt(tau2):.4f} logit")
    print(f"  **I² = {I2:.2f}%**   Q = {Q:.1f} (df={len(sub)-1})")
    print(f"  院校准截距 a_h 分布      P10={np.percentile(sub['a_h'],10):+.3f}  "
          f"中位={sub['a_h'].median():+.3f}  P90={np.percentile(sub['a_h'],90):+.3f}  "
          f"范围 {sub['a_h'].min():+.3f} ~ {sub['a_h'].max():+.3f}")
    print(f"  O/E 比分布              P10={np.percentile(sub['OE'],10):.2f}  "
          f"中位={sub['OE'].median():.2f}  P90={np.percentile(sub['OE'],90):.2f}")
    au = sub.dropna(subset=["auc_sofa"])
    print(f"  逐院判别力 SOFA 单独 AUC P10={np.percentile(au['auc_sofa'],10):.3f}  "
          f"中位={au['auc_sofa'].median():.3f}  P90={np.percentile(au['auc_sofa'],90):.3f}")
    rho, prho = __import__("scipy.stats", fromlist=["s"]).spearmanr(sub["sofa_mean"], sub["obs"])
    print(f"  Q3 病例组合：医院平均 SOFA vs 院死亡率 Spearman ρ = {rho:+.3f} (P={prho:.3g})")
    print(f"     → 病例组合仅解释 ρ²≈{rho**2*100:.1f}% 的排序关系，其余为**残余漂移**")

# ---------- 5. 图 ----------
# 图1/图2 用的统计量（n≥100 且院内事件≥10）
_fig = H[(H["n"] >= 100) & (H["deaths"] >= 10)]
_, tau2_fig, I2_fig, _, _ = dersimonian(_fig["a_h"].values, _fig["se_a"].values)
from scipy.stats import spearmanr
rho_fig, _ = spearmanr(_fig["sofa_mean"], _fig["obs"])

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.unicode_minus": False})
C_BLUE, C_RED, C_GRY = "#1F5C8B", "#C0392B", "#7F8C8D"

# 图1 caterpillar（n≥100 且院内事件≥10，避免 0 事件医院把二分法顶到边界）
fig, ax = plt.subplots(figsize=(7.2, 4.8))
sub = H[(H["n"] >= 100) & (H["deaths"] >= 10)].copy().sort_values("a_h").reset_index(drop=True)
x = np.arange(len(sub))
ax.axhline(0, color="#2C3E50", lw=1.1, ls="--", zorder=1)
ax.vlines(x, sub["a_h"] - 1.96 * sub["se_a"], sub["a_h"] + 1.96 * sub["se_a"],
          color="#C9CFD4", lw=0.75, zorder=2)
sizes = 16 + 46 * np.log10(sub["n"] / sub["n"].min() + 1)
ax.scatter(x, sub["a_h"], s=sizes, c=np.clip(sub["a_h"], -0.9, 0.9),
           cmap="RdBu_r", vmin=-0.9, vmax=0.9, edgecolor="#2C3E50", lw=0.5, zorder=3)
ax.set_xlabel(f"eICU centre (sorted by calibration offset;  k = {len(sub)},  n ≥ 100)", fontsize=9)
ax.set_ylabel("Calibration-in-the-large offset,  $a_h$\n(> 0 = higher mortality than the model predicts)", fontsize=9)
ax.set_title("Discrimination transports, calibration does not\n"
             "the same severity model miscalibrates across eICU centres",
             fontsize=11, fontweight="bold", pad=10)
lo, hi = sub["a_h"].min(), sub["a_h"].max()
ax.set_ylim(lo - 0.28, hi + 0.28)
oe10, oe90 = np.percentile(sub["OE"], 10), np.percentile(sub["OE"], 90)
ax.text(0.015, 0.03,
        f"Hospital O/E ratio:  P10 = {oe10:.2f}   median = {sub['OE'].median():.2f}   P90 = {oe90:.2f}\n"
        f"Between-hospital $I^2$ = {I2_fig:.1f}%;  between-hospital SD = {np.sqrt(tau2_fig):.2f} logit\n"
        f"dot size ∝ log(n);  bars = 95% CI",
        transform=ax.transAxes, fontsize=7.6, color="#34495E",
        bbox=dict(fc="white", ec="#D5D8DC", lw=0.6, pad=4.5))
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
for ext, kw in [(".png", dict(dpi=300)), (".pdf", dict())]:
    fig.savefig(os.path.join(OUT, "路B图1_逐院校准漂移" + ext), bbox_inches="tight", **kw)
plt.close(fig)
print(f"\n[fig] 路B图1_逐院校准漂移（k={len(sub)}，deaths≥10）")

# 图2 病例组合 vs 残余
s2 = H[(H["n"] >= 100) & (H["deaths"] >= 10)].copy()
fig, ax = plt.subplots(figsize=(5.6, 4.6))
sc = ax.scatter(s2["sofa_mean"], s2["obs"], s=18 + 34 * np.log10(s2["n"] / s2["n"].min() + 1),
                c=np.clip(s2["a_h"], -0.9, 0.9), cmap="RdBu_r", vmin=-0.9, vmax=0.9,
                edgecolor="#2C3E50", lw=0.5, alpha=0.92)
_xs = np.linspace(s2["sofa_mean"].min(), s2["sofa_mean"].max(), 60)
ax.plot(_xs, expit(m.intercept_[0] + m.coef_[0, 0] * (_xs - df["sofa"].mean()) / df["sofa"].std()),
        color="#2C3E50", lw=1.3, ls="--",
        label="Expected mortality if case-mix alone\nexplained the differences")
ax.set_xlabel("Hospital mean SOFA score  (case-mix)", fontsize=9)
ax.set_ylabel("Hospital observed mortality", fontsize=9)
ax.set_title("Case-mix explains only part of the drift", fontsize=11, fontweight="bold", pad=10)
ax.legend(fontsize=7.4, loc="lower right", frameon=True, framealpha=0.92)
ax.text(0.02, 0.96, f"Spearman ρ = {rho_fig:+.2f}  (ρ² ≈ {rho_fig**2*100:.0f}%)",
        transform=ax.transAxes, fontsize=8, va="top", color="#34495E",
        bbox=dict(fc="white", ec="#D5D8DC", lw=0.6, pad=3.5))
ax.spines[["top", "right"]].set_visible(False)
cb = fig.colorbar(sc, ax=ax, pad=0.02); cb.set_label("calibration offset $a_h$", fontsize=8)
cb.ax.tick_params(labelsize=7)
fig.tight_layout()
for ext, kw in [(".png", dict(dpi=300)), (".pdf", dict())]:
    fig.savefig(os.path.join(OUT, "路B图2_病例组合vs残余" + ext), bbox_inches="tight", **kw)
plt.close(fig)
print("[fig] 路B图2_病例组合vs残余")

# ---------- 6. 判据 ----------
sub100 = H[H["n"] >= 100]
abar, tau2, I2, Q, seRE = dersimonian(sub100["a_h"].values, sub100["se_a"].values)
ok = (I2 > 50) and (len(sub100) >= 100)
print("\n" + "=" * 78)
print(f"### 判据：I²>50% 且 n≥100 医院≥100 家 → I²={I2:.2f}%，n≥100 家数={len(sub100)} → "
      f"**{'成立' if ok else '不成立'}**")
print("=" * 78)
json.dump(dict(k=len(sub100), I2=I2, tau2=tau2, a_bar=abar, seRE=seRE,
               n_hosp_total=int(H["hospital"].nunique()),
               n_hosp_ge100=int(len(sub100)),
               pooled_auc=float(roc_auc_score(df["y"], df["p"]))),
          open(os.path.join(OUT, "路B_判据.json"), "w", encoding="utf-8"), indent=2)
print("[done] 产物 ->", OUT)
