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
sys.path.insert(0, BASE)
from figures_common import r1

DARK, EDGE, TXT = "#2C3E50", "#2C3E50", "#1B2631"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.2, "axes.unicode_minus": False})

MIMIC = [
    ("MIMIC-IV v3.1 ICU stays\n(n = 94,458)", "#D6EAF8"),
    ("First ICU stay per patient (n = 65,366)", None),
    ("Age \u2265 65 years (n = 35,499)", None),
    ("ICU length of stay \u2265 24 h (n = 28,607)", None),
    ("First stay in MICU or MICU/SICU (n = 8,629)", None),
    ("Excluded: died within\n24 h of ICU\nadmission (n = 35)", "#FDEDEC"),
    ("Excluded: albumin,\nheight and weight\nall missing (n = 15)", "#FDEDEC"),
    ("Analysed cohort (n = 8,579)\nhospital deaths = 1,654 (19.3%)", "#D5F5E3"),
    ("Single centre (BIDMC)\nused for external application of the\neICU-derived model \u2014 no refitting", "#FEF9E7"),
]
EICU = [
    ("eICU-CRD v2.0 unit stays\n(208 hospitals, n = 200,859)", "#D6EAF8"),
    ("First ICU stay per patient (n = 139,367)", None),
    ("Age \u2265 65 years (n = 71,734)", None),
    ("ICU length of stay \u2265 24 h (n = 50,138)", None),
    ("MICU or Med-Surg ICU (n = 31,307)", None),
    ("Excluded: died within\n24 h of ICU\nadmission (n = 7)", "#FDEDEC"),
    ("Excluded: hospital\noutcome status\nmissing (n = 363)", "#FDEDEC"),
    ("Excluded: albumin,\nheight and weight\nall missing (n = 141)", "#FDEDEC"),
    ("Analysed cohort: 187 hospitals\n(n = 30,796; deaths = 3,901, 12.7%)", "#D5F5E3"),
    ("Centres with \u2265 100 patients and \u2265 10 deaths\n\u2192 k = 103 centres used for the\nbetween-centre analyses", "#FEF9E7"),
]

fig, ax = plt.subplots(figsize=(15.0, 13.2))
ax.set_xlim(0, 29.5); ax.set_ylim(0, 30.0); ax.axis("off")
OVERFLOW = []          # 用于绘后自动检测文字是否越框

MAIN_W, EXC_W, EXC_OFF = 8.4, 5.6, 8.7      # 主链宽 / 排除框宽 / 排除框右偏


def box(x, y, w, h, text, fc, fs=7.8, ec=EDGE):
    """画框并检测文字是否越框（超出即告警，避免靠目测）。"""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.010,rounding_size=0.18",
                                fc=(fc or "#FFFFFF"), ec=ec, lw=1.05))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=TXT, linespacing=1.42)
    OVERFLOW.append((text, x, y, w, h, fs))


for col_x, head, steps in [(0.2, "eICU-CRD  \u2010  estimation cohort", EICU),
                           (15.0, "MIMIC-IV  \u2010  external application", MIMIC)]:
    ax.text(col_x + MAIN_W / 2, 29.2, head, ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=TXT)
    ys = np.linspace(25.7, 1.0, len(steps))
    hh = 2.40
    last_incl = None                                   # 最近一个"纳入"框（主链节点）
    for i, ((txt, fc), yy) in enumerate(zip(steps, ys)):
        excluded = txt.startswith("Excluded")
        if excluded:
            # CONSORT 式：排除项外挂至主链右侧，斜向箭头指出，不进入主链
            ex_x = col_x + EXC_OFF
            box(ex_x, yy + 0.02, EXC_W, hh - 0.04, txt, fc, fs=7.2, ec="#B03A2E")
            if last_incl is not None:
                ax.add_patch(FancyArrowPatch(
                    (col_x + MAIN_W * 0.72, last_incl), (ex_x, yy + hh / 2),
                    arrowstyle="-|>", mutation_scale=12, color="#B03A2E", lw=1.0,
                    connectionstyle="arc3,rad=0.10", shrinkA=1, shrinkB=1))
        else:
            box(col_x, yy, MAIN_W, hh, txt, fc)
            if last_incl is not None:
                ax.add_patch(FancyArrowPatch((col_x + MAIN_W / 2, last_incl),
                                             (col_x + MAIN_W / 2, yy + hh),
                                             arrowstyle="-|>", mutation_scale=13,
                                             color=EDGE, lw=1.05))
            last_incl = yy



# ---------- 自动检测文字是否越框（避免靠目测）----------
fig.canvas.draw()
_ren = fig.canvas.get_renderer()
_bad = []
for _txt, _x, _y, _w, _h, _fs in OVERFLOW:
    for _t in ax.texts:
        if _t.get_text() != _txt:
            continue
        _bb = _t.get_window_extent(renderer=_ren).transformed(ax.transData.inverted())
        if _bb.width > _w * 0.98 or _bb.height > _h * 0.94:
            _bad.append((_txt.replace("\n", " / ")[:44], round(_bb.width, 2), _w,
                         round(_bb.height, 2), _h))
        break
if _bad:
    print("[越框告警] %d 个文本超出方框（需加宽框或缩短文案）:" % len(_bad))
    for _n, _ow, _w, _oh, _h in _bad:
        print("    %-46s 宽 %.2f > %.2f  或  高 %.2f > %.2f" % (_n, _ow, _w, _oh, _h))
else:
    print("[越框检测] 全部文本在方框内 ✔")

fig.savefig(os.path.join(FG, "Fig1_两库筛选流程图.png"), dpi=600, bbox_inches="tight")
fig.savefig(os.path.join(FG, "Fig1_两库筛选流程图.pdf"), bbox_inches="tight")
plt.close(fig)
print("[saved] Fig1_两库筛选流程图")
