# -*- coding: utf-8 -*-
"""路B 第二批出图：图8 时间稳定性(split-half) / 图9 规模分层 / 图10 临床影响"""
import io, sys, os, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST, FG = os.path.join(BASE, "03_统计"), os.path.join(BASE, "04_图表")
sys.path.insert(0, BASE)
from figures_common import r1

R = json.load(open(os.path.join(ST, "batch2_results.json"), encoding="utf-8"))
BLUE, RED, GRAY, DARK, ORG = "#2C6E9B", "#C0392B", "#9AA5B1", "#1B2631", "#E67E22"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.unicode_minus": False,
                     "axes.linewidth": 0.8})


def save(fig, stem):
    fig.savefig(os.path.join(FG, stem + ".png"), dpi=600, bbox_inches="tight")
    fig.savefig(os.path.join(FG, stem + ".pdf"), bbox_inches="tight")
    plt.close(fig)
    print("[saved]", stem)


# ═══════════ 图8 split-half ═══════════
F = pd.read_csv(os.path.join(ST, "temporal_split_half.csv"))
rf = R["F"]
fig, ax = plt.subplots(figsize=(5.9, 5.2))
lo = min(F["a14"].min(), F["a15"].min()) - 0.15
hi = max(F["a14"].max(), F["a15"].max()) + 0.15
ax.plot([lo, hi], [lo, hi], color=DARK, lw=1.1, ls="--", zorder=2,
        label="perfect year-to-year stability")
ax.axhline(0, color=GRAY, lw=0.7); ax.axvline(0, color=GRAY, lw=0.7)
# 最小二乘拟合线：斜率 < 1 且整体位于对角线下方，把「系统性下移」这一正文论点可视化
sl, ic = np.polyfit(F["a14"], F["a15"], 1)
xs = np.array([lo, hi])
ax.plot(xs, sl * xs + ic, color=RED, lw=1.5, zorder=4,
        label=f"least-squares fit (slope {sl:.2f})")
sc = ax.scatter(F["a14"], F["a15"], s=30, c=np.clip(F["da"], -0.9, 0.9), cmap="RdBu_r",
                vmin=-0.9, vmax=0.9, edgecolor="#33414D", lw=0.55, alpha=0.80, zorder=3)
ax.set_xlabel("Calibration offset, 2014  ($a_h^{2014}$)", fontsize=9.4)
ax.set_ylabel("Calibration offset, 2015  ($a_h^{2015}$)", fontsize=9.4)
ax.text(0.025, 0.975,
        "Pearson $r$ = %.2f\n$r^2$ = %.2f\n"
        "k = %d centres\n"
        "median $|\\Delta a|$ = %.2f\n"
        "fit slope = %.2f\n"
        "temporal share of\nbetween-centre variance\n= %.0f%%"
        % (rf["r"], rf["r"] ** 2, rf["k"], rf["da_med"], sl, rf["temporal_share_pct"]),
        transform=ax.transAxes, fontsize=8.0, va="top", color=DARK,
        bbox=dict(fc="white", ec="#D5D8DC", lw=0.5, pad=4.0))
ax.legend(fontsize=7.4, frameon=False, loc="lower right")
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
ax.spines[["top", "right"]].set_visible(False)
cb = fig.colorbar(sc, ax=ax, pad=0.02)
cb.set_label("$\\Delta a$  (2015 − 2014)", fontsize=8)
cb.ax.tick_params(labelsize=7)
save(fig, "SuppFigS3_同一中心两年校准偏移的稳定性")

# ═══════════ 图9 规模分层 ═══════════
G = R["G"]
_key = {"小": "Small", "中": "Medium", "大": "Large"}
labs = ["Small", "Medium", "Large"]
_src = [G["小"], G["中"], G["大"]]
G = {_key[k]: v for k, v in G.items()}
fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.3))
ax = axes[0]
xs = np.arange(3)
i2 = [G[l]["I2"] for l in labs]; t2 = [G[l]["tau2"] for l in labs]
b = ax.bar(xs - 0.19, i2, width=0.36, color=BLUE, edgecolor=DARK, lw=0.7, zorder=3, label="$I^2$ (%)")
for xx, v in zip(xs - 0.19, i2):
    ax.text(xx, v + 1.6, f"{r1(v)}%", ha="center", fontsize=8.4, fontweight="bold", color=DARK)
ax.axhline(50, color=RED, lw=1.0, ls="--")
ax.text(0.02, 52.5, "50% threshold for substantial heterogeneity", color=RED, fontsize=7.2, ha="left")
ax.set_ylabel("$I^2$  (%)", fontsize=9.2); ax.set_ylim(0, 108)
ax.set_xticks(xs); ax.set_xticklabels([f"{l} centre\nmedian n = {G[l]['n_med']:.0f}" for l in
                                       ["Small", "Medium", "Large"]], fontsize=8.4)
ax2 = ax.twinx()
ax2.plot(xs, t2, marker="o", color=ORG, lw=1.8, ms=6, zorder=4, label="$\\tau^2$")
for xx, v in zip(xs, t2):
    ax2.text(xx, v + 0.007, f"{v:.3f}", ha="center", fontsize=8.2, color=ORG, fontweight="bold")
ax2.set_ylabel("$\\tau^2$  (between-centre variance)", fontsize=9.2, color=ORG)
ax2.tick_params(axis="y", colors=ORG, labelsize=8); ax2.set_ylim(0, 0.18)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left", frameon=False)
ax.spines[["top"]].set_visible(False); ax2.spines[["top"]].set_visible(False)

ax = axes[1]
HL = R["H"]
pts = [h["pt"] for h in HL]
ppv = [[h["ppv_p10"], h["ppv_med"], h["ppv_p90"]] for h in HL]
for i, (pt, v) in enumerate(zip(pts, ppv)):
    ax.plot([i, i], [v[0], v[2]], color=BLUE, lw=1.6, solid_capstyle="butt", zorder=3)
    ax.plot([i], [v[1]], marker="s", ms=7, color=BLUE, zorder=4,
            markeredgecolor=DARK, markeredgewidth=0.6)
    ax.annotate(f"{v[0]:.0f}–{v[2]:.0f}%", (i, v[2]), textcoords="offset points",
                xytext=(6, -2), fontsize=7.2, color=BLUE)
ax.axhline(100 * 0.1267, color=RED, lw=1.0, ls="--")
ax.text(0.5, 100 * 0.1267 + 2.0, "cohort mortality 12.7%", color=RED, fontsize=7.2, ha="center",
        bbox=dict(fc="white", ec="none", pad=1.6))
ax.set_xticks(np.arange(len(pts)))
ax.set_xticklabels([f"{p:.2f}" for p in pts], fontsize=8.6)
ax.set_xlabel("Decision threshold  $p_t$", fontsize=9.2)
ax.set_ylabel("Observed mortality among\nthose flagged  (%)", fontsize=9.0)
ax.set_ylim(-16, 112)
ax.spines[["top", "right"]].set_visible(False)
fig.subplots_adjust(left=0.085, right=0.965, top=0.965, bottom=0.145, wspace=0.42)
save(fig, "Fig5_规模分层与临床影响")
print("[done]")
