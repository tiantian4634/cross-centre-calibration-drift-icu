# -*- coding: utf-8 -*-
"""路B 图10：分层收缩(EB) vs 朴素重校准 —— 学习曲线四策略对比"""
import io, sys, os, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST, FG = os.path.join(BASE, "03_统计"), os.path.join(BASE, "04_图表")
S = pd.DataFrame(json.load(open(os.path.join(ST, "shrinkage_summary.json"), encoding="utf-8"))["rows"])

# 标注锚点由数据算出，并校验标注所声称的结论是否仍成立
def _v(strat, m, col):
    s = S[(S["strat"] == strat) & (S["m"] == m)][col]
    if s.empty:
        raise ValueError("找不到 strat=%s m=%s" % (strat, m))
    return float(s.iloc[0])

BASE0 = _v("S0", 0, "ra_med")      # 完全不校准的残余 |a|
EB_M25 = _v("S3", 25, "ra_med")    # EB 在 m=25 的残余 |a|
if not (EB_M25 < BASE0):
    raise AssertionError(
        f"标注声称『EB 在 m=25 已优于不校准』，但实测 EB={EB_M25:.4f} ≥ S0={BASE0:.4f}，"
        "结论不再成立，须改写标注文字")
print(f"[图10 数据核对] S0 基线={BASE0:.4f}  S3@m25={EB_M25:.4f}  (EB < S0 ✔)")

BLUE, RED, GRAY, DARK, ORG, TEAL = "#2C6E9B", "#C0392B", "#9AA5B1", "#1B2631", "#E67E22", "#1E8449"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.unicode_minus": False,
                     "axes.linewidth": 0.8})

STY = {"S0": dict(c=GRAY, mk="o", ls=":", lw=1.4, lab="S0   No recalibration"),
       "S1": dict(c=BLUE, mk="o", ls="-", lw=1.7, lab="S1   Naive, intercept only"),
       "S2": dict(c=RED, mk="s", ls="-", lw=1.4, lab="S2   Naive, intercept + slope"),
       "S3": dict(c=TEAL, mk="D", ls="-", lw=2.2, lab="S3   Empirical-Bayes shrinkage")}

fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
ax = axes[0]
for s in ["S0", "S1", "S2", "S3"]:
    d = S[S["strat"] == s].sort_values("m")
    st = STY[s]
    ax.plot(d["m"], d["ra_med"], marker=st["mk"], ms=5.5, color=st["c"], lw=st["lw"],
            ls=st["ls"], label=st["lab"], zorder=4 if s == "S3" else 3)
    ax.fill_between(d["m"], d["ra_med"], d["ra_p90"], color=st["c"], alpha=0.10, zorder=1)
d0 = S[(S["strat"] == "S0") & (S["m"] == 0)]["ra_med"].iloc[0]
ax.axhline(d0, color=GRAY, lw=1.0, ls=":")
ax.annotate("no recalibration at all\n$|a|$ = %.2f" % d0, xy=(0, d0), xytext=(112, d0 + 0.028),
            fontsize=7.6, color=GRAY, ha="left")
ax.annotate("EB already beats\nno recalibration\nat m = 25", xy=(25, EB_M25), xytext=(46, 0.055),
            fontsize=7.8, color=TEAL, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))
ax.set_xlabel("Local patients used for recalibration  ($m$)", fontsize=9.4)
ax.set_ylabel("Residual miscalibration  $|a|$\n(median; band → P90)", fontsize=9.0)
ax.set_xlim(-8, 212); ax.set_ylim(0, 0.72)
ax.legend(fontsize=7.8, frameon=False, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)

ax = axes[1]
for s in ["S0", "S1", "S2", "S3"]:
    d = S[S["strat"] == s].sort_values("m")
    st = STY[s]
    ax.plot(d["m"], d["ok11"], marker=st["mk"], ms=5.5, color=st["c"], lw=st["lw"],
            ls=st["ls"], zorder=4 if s == "S3" else 3)
d0 = S[(S["strat"] == "S0") & (S["m"] == 0)]["ok11"].iloc[0]
ax.axhline(d0, color=GRAY, lw=1.0, ls=":")
ax.annotate(f"no recalibration: {d0:.0f}%", xy=(0, d0), xytext=(60, d0 + 1.6), fontsize=7.6, color=GRAY)
ax.axhline(50, color=DARK, lw=0.8, ls="--", alpha=0.5)
ax.text(206, 51.5, "50%", fontsize=7.2, color=DARK, ha="right", alpha=0.7)
ax.set_xlabel("Local patients used for recalibration  ($m$)", fontsize=9.4)
ax.set_ylabel("Recalibration attempts landing\nwithin ±10%  (%)", fontsize=9.0)
ax.set_xlim(-8, 212); ax.set_ylim(5, 62)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(FG, "图10_分层收缩重校准.png"), dpi=600, bbox_inches="tight")
fig.savefig(os.path.join(FG, "图10_分层收缩重校准.pdf"), bbox_inches="tight")
plt.close(fig)
print("[saved] 图10_分层收缩重校准")

# 顺带打印 lambda 统计
R = pd.read_csv(os.path.join(ST, "shrinkage_raw.csv"))
L = R[R["m"] > 0].groupby("m")["lam"].median()
print("\n[收缩强度 λ 中位]（λ 越小收缩越强）")
for m, v in L.items():
    print(f"   m={int(m):>4}: λ = {v:.3f}")
