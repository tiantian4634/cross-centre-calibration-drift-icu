# -*- coding: utf-8 -*-
"""路B 出图：图3 三评分caterpillar / 图4 判别稳·校准漂 / 图5 病例组合阶梯 / 图6 MIMIC 定位"""
import io, sys, os, json
import numpy as np, pandas as pd
from scipy.special import expit, logit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST, FG = os.path.join(BASE, "03_统计"), os.path.join(BASE, "04_图表")
sys.path.insert(0, BASE)
from figures_common import r1
AUC_CI = json.load(open(os.path.join(ST, "pooled_auc_ci.json"), encoding="utf-8"))

os.makedirs(FG, exist_ok=True)

H = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
R = json.load(open(os.path.join(ST, "drift_results.json"), encoding="utf-8"))

BLUE, RED, GRAY, DARK = "#2C6E9B", "#C0392B", "#9AA5B1", "#1B2631"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.linewidth": 0.8, "axes.unicode_minus": False,
                     "xtick.major.width": 0.8, "ytick.major.width": 0.8})


def save(fig, stem):
    fig.savefig(os.path.join(FG, stem + ".png"), dpi=600, bbox_inches="tight")
    fig.savefig(os.path.join(FG, stem + ".pdf"), bbox_inches="tight")
    plt.close(fig)
    print("[saved]", stem)


# ══════════════════ 图3 三联 caterpillar ══════════════════
fig = plt.figure(figsize=(9.4, 3.7))
gs = GridSpec(1, 3, width_ratios=[1, 1, 1], wspace=0.28, left=0.075, right=0.985, top=0.96, bottom=0.16)
for i, name in enumerate(["SOFA", "OASIS", "SAPS-II"]):
    ax = fig.add_subplot(gs[0, i])
    d = H[H["score"] == name].sort_values("a_h").reset_index(drop=True)
    x = np.arange(len(d))
    ax.axhline(0, color=DARK, lw=1.0, ls="--", zorder=1)
    ax.vlines(x, d["a_h"] - 1.96 * d["se_a"], d["a_h"] + 1.96 * d["se_a"],
              color="#B4BAC1", lw=0.7, zorder=2)
    sz = 13 + 30 * np.log10(d["n"] / d["n"].min() + 1)
    ax.scatter(x, d["a_h"], s=sz, c=np.clip(d["a_h"], -0.85, 0.85),
               cmap="RdBu_r", vmin=-0.85, vmax=0.85, edgecolor="#33414D", lw=0.45, zorder=3)
    r = R["scores"][name]
    ax.set_title(f"{name}", fontsize=11, fontweight="bold", pad=6)
    ax.text(0.03, 0.965, f"$I^2$ = {r1(r['I2'])}%\nAUC {r['pooled_auc']:.3f} ({AUC_CI[name]['lo']}–{AUC_CI[name]['hi']})",
            transform=ax.transAxes, fontsize=8.2, va="top", color=DARK,
            bbox=dict(fc="white", ec="#D5D8DC", lw=0.5, pad=3.2))
    ax.text(0.97, 0.035, f"P10–P90 O/E\n{r['OE_p10']:.2f} – {r['OE_p90']:.2f}",
            transform=ax.transAxes, fontsize=7.4, va="bottom", ha="right", color=DARK,
            bbox=dict(fc="white", ec="none", pad=2.2))
    ax.set_ylim(-0.95, 1.45)
    ax.set_xlim(-4, len(d) + 3)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel(f"centre (sorted, k={r['k']})", fontsize=8.2)
    if i == 0:
        ax.set_ylabel("Calibration-in-the-large offset $a_h$\n"
                      "(> 0 = more deaths than predicted)", fontsize=8.6)
    ax.spines[["top", "right"]].set_visible(False)
save(fig, "Fig2_三评分校准漂移对比")

# ══════════════════ 图4 判别稳 · 校准漂 ══════════════════
d = H[H["score"] == "SOFA"].copy()
fig = plt.figure(figsize=(7.6, 4.6))
gs = GridSpec(2, 2, width_ratios=[3.2, 1], height_ratios=[1, 3.2],
              wspace=0.10, hspace=0.10, left=0.10, right=0.955, top=0.98, bottom=0.115)
ax = fig.add_subplot(gs[1, 0]); axt = fig.add_subplot(gs[0, 0], sharex=ax); axr = fig.add_subplot(gs[1, 1], sharey=ax)
ax.scatter(d["auc"], d["OE"], s=22, c=np.clip(d["a_h"], -0.85, 0.85), cmap="RdBu_r",
           vmin=-0.85, vmax=0.85, edgecolor="#33414D", lw=0.5, alpha=0.72, zorder=3)
ax.axhline(1.0, color=DARK, lw=1.0, ls="--", zorder=1)
axv = float(R["scores"]["SOFA"]["pooled_auc"])
ax.axvline(axv, color=RED, lw=1.0, ls=":", zorder=1)
ax.set_xlabel("Per-hospital AUC  (discrimination)", fontsize=9.2)
ax.set_ylabel("Per-hospital O/E ratio  (calibration)", fontsize=9.2)
axt.text(0.5, 1.055, "pooled AUC %.3f  (95%% CI %.3f\u2013%.3f)" % (axv, AUC_CI["SOFA"]["lo"], AUC_CI["SOFA"]["hi"]),
         transform=axt.transAxes, ha="center", va="bottom", fontsize=7.6, color=RED, fontweight="bold")
ax.text(0.835, 1.035, "perfect calibration", fontsize=7.4, color=DARK, ha="right")
ax.text(0.985, 0.96,
        "AUC: 0.649–0.812 (P10–P90 width 0.163)\nO/E: 0.69–1.54 (P10–P90 ratio 2.2-fold)",
        transform=ax.transAxes, fontsize=8.2, va="top", ha="right", color=DARK,
        bbox=dict(fc="white", ec="#D5D8DC", lw=0.5, pad=3.5))
axt.hist(d["auc"], bins=18, color=BLUE, alpha=0.85, edgecolor="white", lw=0.4)
axt.axvline(axv, color=RED, lw=1.0, ls=":")
axt.set_ylabel("n", fontsize=8); axt.tick_params(labelbottom=False, labelsize=7.5)
axr.hist(d["OE"], bins=18, orientation="horizontal", color=RED, alpha=0.8, edgecolor="white", lw=0.4)
axr.axhline(1.0, color=DARK, lw=1.0, ls="--")
axr.set_xlabel("n", fontsize=8); axr.tick_params(labelleft=False, labelsize=7.5)
for s in ["top", "right"]:
    axt.spines[s].set_visible(False); axr.spines[s].set_visible(False)
ax.set_xlim(0.62, 0.84); ax.set_ylim(0.55, 1.72)
save(fig, "Fig3_判别稳与校准漂")

# ══════════════════ SuppFig S1 病例组合阶梯 ══════════════════
L = R["ladder"]
tags = list(L.keys())
i2 = [L[t]["I2"] for t in tags]
aucv = [L[t]["AUC"] for t in tags]
# A5 参照柱：在 M3 的同一患者子集、同一中心集合上，只把模型换回 M1（SOFA 单评分）。
# 若其 I² 接近 M1 而非 M3，则 M3 的下降可归因于协变量本身，而非分析集变化。
CM = json.load(open(os.path.join(ST, "casemix_set_sensitivity.json"), encoding="utf-8"))
REF_I2, REF_K, REF_N = CM["I2_m1_same_subset"], CM["m3"]["k"], CM["m3"]["n"]
print("[SuppFigS1] 参照柱 I²=%.2f%%（同 %d 中心 / %d 患者）" % (REF_I2, REF_K, REF_N))

i2 = i2 + [REF_I2]
aucv = aucv + [None]
tags_x = ["M1\nSOFA", "M2\n+ age, sex",
          "M3\n+ comorbidity,\ninvasive ventilation\nn = 27,236; k = %d" % REF_K,
          "M1 reference\nsame patients\nand centres\n(n = 27,236; k = %d)" % REF_K]
COLS = [BLUE, "#5B8FB9", GRAY, "#D5D8DC"]
fig, ax = plt.subplots(figsize=(7.9, 4.2))
xx = np.arange(len(i2))
bars = ax.bar(xx, i2, width=0.58, color=COLS, edgecolor=DARK, lw=0.7, zorder=3)
for b, v, a in zip(bars, i2, aucv):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.6, "$I^2$ = %s%%" % r1(v),
            ha="center", fontsize=9.5, fontweight="bold", color=DARK)
    if a is not None:
        ax.text(b.get_x() + b.get_width() / 2, v / 2, "AUC\n%.3f" % a, ha="center",
                va="center", fontsize=9, color="white", fontweight="bold")
ax.axhline(50, color=RED, lw=1.1, ls="--", zorder=2)
ax.text(-0.42, 51.5, "$I^2$ = 50% (substantial heterogeneity)",
        color=RED, fontsize=7.4, ha="left", va="bottom")
ax.set_xticks(xx)
ax.set_xticklabels(tags_x, fontsize=8.2)
ax.set_ylabel("Between-centre heterogeneity $I^2$ (%)", fontsize=9.4)
ax.set_ylim(0, 92)
ax.set_xlim(-0.6, len(i2) - 0.4)
ax.spines[["top", "right"]].set_visible(False)
fig.subplots_adjust(left=0.105, right=0.985, top=0.96, bottom=0.235)
save(fig, "SuppFigS1_病例组合阶梯")

# ══════════════════ 图6 MIMIC 定位 ══════════════════
d = H[H["score"] == "SOFA"]
aM = R["mimic"]["a"]; pct = R["mimic"]["percentile"]
fig, ax = plt.subplots(figsize=(7.0, 2.9))
ax.axvline(0, color=DARK, lw=1.0, ls="--")
rng = np.random.default_rng(7)
jit = rng.uniform(-0.16, 0.16, len(d))
ax.scatter(d["a_h"], jit + 0.55, s=14, c=np.clip(d["a_h"], -0.85, 0.85), cmap="RdBu_r",
           vmin=-0.85, vmax=0.85, edgecolor="#33414D", lw=0.4, alpha=0.85, zorder=3)
ax.scatter([aM], [0.18], marker="D", s=95, color="#E67E22", edgecolor=DARK, lw=0.9, zorder=5)
ax.annotate(f"MIMIC-IV (single centre, BIDMC)\n$a$ = {aM:+.3f}  ·  {pct:.0f}th percentile of eICU centres\n"
            f"observed {100*R['mimic']['obs']:.1f}% vs predicted {100*R['mimic']['exp']:.1f}%  (O/E {R['mimic']['OE']:.2f})",
            xy=(aM, 0.22), xytext=(aM + 0.20, -0.14), fontsize=8, color="#8E4B10",
            arrowprops=dict(arrowstyle="->", color="#8E4B10", lw=1.0))
ax.text(0.998, 0.945, "103 eICU centres  ·  AUC %.3f (eICU) vs %.3f (MIMIC)"
            % (R["mimic"]["auc_eicu"], R["mimic"]["auc_mimic"]),
            transform=ax.transAxes, ha="right", fontsize=7.6, color="#5B6672",
            bbox=dict(fc="white", ec="none", pad=2.2), zorder=6)
ax.set_yticks([]); ax.set_ylim(-0.35, 0.95)
ax.set_xlabel("Calibration-in-the-large offset $a_h$  (> 0 = more deaths than predicted)", fontsize=9.2)
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, "SuppFigS2_MIMIC在多中心分布中的位置")
print("\n[done] 图件 ->", FG)
