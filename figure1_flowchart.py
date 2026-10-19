# -*- coding: utf-8 -*-
"""路B 图1：两库患者筛选流程图（CONSORT 式）。数字全部取自既有计数报告，不重新统计。"""
import io, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
SRCDIR = os.path.join(BASE, "09_路B_跨院校准")
FG = os.path.join(SRCDIR, "04_图表")
DARK, EDGE, TXT = "#2C3E50", "#2C3E50", "#1B2631"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.2, "axes.unicode_minus": False})

MIMIC = [
    ("MIMIC-IV v3.1 ICU stays\n(n = 94,458)", "#D6EAF8"),
    ("First ICU stay per patient (n = 65,366)", None),
    ("Age \u2265 65 years (n = 35,499)", None),
    ("ICU length of stay \u2265 24 h (n = 28,607)", None),
    ("First stay in MICU or MICU/SICU (n = 8,629)", None),
    ("Excluded: died within 24 h of ICU admission (n = 35)", "#FDEDEC"),
    ("Excluded: albumin, height and weight\nall missing (n = 15)", "#FDEDEC"),
    ("Analysed cohort (n = 8,579)\nhospital deaths = 1,654 (19.3%)", "#D5F5E3"),
    ("Single centre (BIDMC)\nused for external application of the\neICU-derived model \u2014 no refitting", "#FEF9E7"),
]
EICU = [
    ("eICU-CRD v2.0 unit stays\n(208 hospitals, n = 200,859)", "#D6EAF8"),
    ("First ICU stay per patient (n = 139,367)", None),
    ("Age \u2265 65 years (n = 71,734)", None),
    ("ICU length of stay \u2265 24 h (n = 50,138)", None),
    ("MICU or Med-Surg ICU (n = 31,307)", None),
    ("Excluded: died within 24 h of ICU admission (n = 7)", "#FDEDEC"),
    ("Excluded: hospital outcome status missing (n = 363)", "#FDEDEC"),
    ("Excluded: albumin, height and weight\nall missing (n = 141)", "#FDEDEC"),
    ("Analysed cohort: 187 hospitals\n(n = 30,796; deaths = 3,901, 12.7%)", "#D5F5E3"),
    ("Centres with \u2265 100 patients and \u2265 10 deaths\n\u2192 k = 103 centres used for the\nbetween-centre analyses", "#FEF9E7"),
]

fig, ax = plt.subplots(figsize=(11.6, 9.2))
ax.set_xlim(0, 20); ax.set_ylim(0, 25.0); ax.axis("off")


def box(x, y, w, h, text, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.010,rounding_size=0.18",
                                fc=(fc or "#FFFFFF"), ec=EDGE, lw=1.05))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=8.0, color=TXT, linespacing=1.45)


for col_x, head, steps in [(0.3, "eICU-CRD  \u2010  estimation cohort", EICU),
                           (10.5, "MIMIC-IV  \u2010  external application", MIMIC)]:
    ax.text(col_x + 4.5, 24.15, head, ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=TXT)
    ys = np.linspace(21.6, 1.2, len(steps))
    hh = 1.55 if len(steps) == 10 else 1.85
    for i, ((txt, fc), yy) in enumerate(zip(steps, ys)):
        box(col_x, yy, 9.0, hh, txt, fc)
        if i > 0:
            ax.add_patch(FancyArrowPatch((col_x + 4.5, ys[i - 1]), (col_x + 4.5, yy + hh),
                                         arrowstyle="-|>", mutation_scale=13,
                                         color=EDGE, lw=1.05))

fig.savefig(os.path.join(FG, "Fig1_两库筛选流程图.png"), dpi=600, bbox_inches="tight")
fig.savefig(os.path.join(FG, "Fig1_两库筛选流程图.pdf"), bbox_inches="tight")
plt.close(fig)
print("[saved] Fig1_两库筛选流程图")
