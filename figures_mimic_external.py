# -*- coding: utf-8 -*-
"""路B 图11：EB 收缩方案的内部(LOO)与外部(MIMIC)验证并列"""
import io, sys, os, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST, FG = os.path.join(BASE, "03_统计"), os.path.join(BASE, "04_图表")
S_int = pd.DataFrame(json.load(open(os.path.join(ST, "shrinkage_summary.json"), encoding="utf-8"))["rows"])
M = json.load(open(os.path.join(ST, "mimic_external_summary.json"), encoding="utf-8"))
S_ext = pd.DataFrame(M["rows"])
BLUE, GRAY, DARK, TEAL = "#2C6E9B", "#9AA5B1", "#1B2631", "#1E8449"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.unicode_minus": False,
                     "axes.linewidth": 0.8})

fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
STY = {"S0": dict(c=GRAY, ls=":", mk="o", lab="S0  no recalibration"),
       "S1": dict(c=BLUE, ls="-", mk="o", lab="S1  naive, intercept only"),
       "S3": dict(c=TEAL, ls="-", mk="D", lab="S3  empirical-Bayes shrinkage")}

# 左：eICU 内部（LOO）
ax = axes[0]
for s in ["S0", "S1", "S3"]:
    d = S_int[S_int["strat"] == s].sort_values("m")
    st = STY[s]
    ax.plot(d["m"], d["ok11"], marker=st["mk"], ms=6, color=st["c"], lw=2.1 if s == "S3" else 1.6,
            ls=st["ls"], label=st["lab"], zorder=4 if s == "S3" else 3)
d0 = S_int[(S_int["strat"] == "S0") & (S_int["m"] == 0)]["ok11"].iloc[0]
ax.axhline(d0, color=GRAY, lw=1.0, ls=":")
ax.text(206, d0 + 1.6, f"{d0:.0f}%", fontsize=7.4, color=GRAY, ha="right")
ax.set_title("Internal (103 eICU centres)", fontsize=10.0, fontweight="bold", pad=8)
ax.set_xlim(-10, 212); ax.set_ylim(4, 42)
ax.legend(fontsize=7.6, frameon=False, loc="lower right")
ax.annotate("shrinkage already beats\nno recalibration at $m$ = 25",
            xy=(25, 23.4), xytext=(6, 31.5), fontsize=7.6, color=TEAL, fontweight="bold",
            ha="left", arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.9))

# 右：MIMIC 外部
ax = axes[1]
for s in ["S0", "S1", "S3"]:
    d = S_ext[S_ext["strat"] == s].sort_values("m")
    st = STY[s]
    ax.plot(d["m"], d["ok11"], marker=st["mk"], ms=6, color=st["c"], lw=2.3 if s == "S3" else 1.7,
            ls=st["ls"], zorder=4 if s == "S3" else 3)
d0 = S_ext[(S_ext["strat"] == "S0") & (S_ext["m"] == 0)]["ok11"].iloc[0]
ax.axhline(d0, color=GRAY, lw=1.0, ls=":")
ax.text(300, d0 + 2.5, f"no recalibration: {d0:.0f}%", fontsize=7.4, color=GRAY, ha="left")
ax.annotate("S3 at $m$=25 (53.5%)\n≈ S1 at $m$=200 (53.0%)",
            xy=(25, 53.5), xytext=(95, 26), fontsize=7.8, color=TEAL, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))
ax.set_title("External (MIMIC-IV)", fontsize=10.0, fontweight="bold", pad=8)
ax.set_xlim(-10, 412); ax.set_ylim(-6, 92)
ax.text(0.03, 0.975, f"$\\bar a$ = {M['abar_eicu']:+.3f},  $\\tau^2$ = {M['tau2_eicu']:.3f}  (both from eICU)\n"
        f"true offset to recover $a^{{*}}$ = {M['a_star']:+.3f}",
        transform=ax.transAxes, fontsize=7.6, va="top", color=DARK,
        bbox=dict(fc="white", ec="#D5D8DC", lw=0.5, pad=3.5))

for a_ in axes:
    a_.set_xlabel("Local patients used for recalibration  ($m$)", fontsize=9.4)
    a_.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("Recalibration attempts landing\nwithin ±10%  (%)", fontsize=9.0)
fig.tight_layout()
fig.savefig(os.path.join(FG, "图11_收缩方案的内外部验证.png"), dpi=600, bbox_inches="tight")
fig.savefig(os.path.join(FG, "图11_收缩方案的内外部验证.pdf"), bbox_inches="tight")
plt.close(fig)
print("[saved] 图11_收缩方案的内外部验证")

# 关键对照表
print("\n=== 关键对照：EB 用 m 例 ≈ 朴素用多少例？===")
for tgt in [25, 50]:
    v_ext = S_ext[(S_ext["strat"] == "S3") & (S_ext["m"] == tgt)]["ok11"].iloc[0]
    hit = S_ext[(S_ext["strat"] == "S1") & (S_ext["ok11"] >= v_ext)]
    if len(hit):
        print(f"   外部(MIMIC)：S3 用 m={tgt} → {v_ext:.1f}%；S1 需要 m={int(hit['m'].min())} 才达到")
    else:
        print(f"   外部(MIMIC)：S3 用 m={tgt} → {v_ext:.1f}%；S1 在 m≤400 内从未达到")
