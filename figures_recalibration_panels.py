# -*- coding: utf-8 -*-
"""合并主图 Fig.5（原 Fig.4 + Fig.6 + Fig.7 三图合一，2×2 四面板）——「本地重校准 × 小样本 × EB 收缩」

面板（2×2，按叙事线分两列）：
  左列 = 分析 E（朴素重校准学习曲线，100 次重抽样）
     (a) ±10% 达标率：S1 vs S2，S0 参照线、50% 事前判据线、各 m 贡献中心数 k
     (b) 残余失校准 |a|（中位；带→P90）：S1/S2
  右列 = 分析 I + J（EB 收缩，200 次配对）
     (c) eICU 内部（LOO 交叉拟合）：S0/S1/S2/S3 + m=25 配对差 +9.05 pp
     (d) 迁移到 MIMIC-IV（ā、tau² 完全固定自 eICU）：S0/S1/S3 + "25 例收缩 ≈ 150 例朴素"

设计约束（与全套图件一致）：
  * 图内**不得**出现主标题、解释性副标题、图底文字注释 —— 说明全部进图注；
  * 面板标识 (a)(b)(c)(d) 允许；
  * 标注数值一律由数据算出，不写死；关键结论加断言校验；
  * Okabe–Ito 色盲安全配色。
"""
import io, sys, os, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST, FG = os.path.join(BASE, "03_统计"), os.path.join(BASE, "04_图表")
sys.path.insert(0, BASE)

LC = pd.DataFrame(json.load(open(os.path.join(ST, "learning_curve_summary.json"), encoding="utf-8")))
_MSH = json.load(open(os.path.join(ST, "shrinkage_summary.json"), encoding="utf-8"))
SH = pd.DataFrame(_MSH["rows"])
MM = json.load(open(os.path.join(ST, "mimic_external_summary.json"), encoding="utf-8"))
MX = pd.DataFrame(MM["rows"])


def _v(df, strat, m, col):
    s = df[(df["strat"] == strat) & (df["m"] == m)][col]
    if s.empty:
        raise ValueError("找不到 strat=%s m=%s col=%s" % (strat, m, col))
    return float(s.iloc[0])


# ---------- 数据守卫（改结果时若断言失效，标注文字必须重写而不是静默过图） ----------
S0_OK = _v(SH, "S0", 0, "ok11")            # 不校准基线 21.4%
E_S1_25 = _v(LC, "S1", 25, "within_09_11")   # 分析 E：朴素 15.3%
E_S2_25 = _v(LC, "S2", 25, "within_09_11")   # 分析 E：双参数 13.7%
I_S1_25 = _v(SH, "S1", 25, "ok11")          # 分析 I：朴素 15.5%
I_S3_25 = _v(SH, "S3", 25, "ok11")          # 分析 I：EB 24.3%
J_S1_25 = _v(MX, "S1", 25, "ok11")          # MIMIC 朴素 23.5%
J_S3_25 = _v(MX, "S3", 25, "ok11")          # MIMIC EB 47.0%
print("[数据核对] S0=%.1f%% | E: S1@25=%.1f%% S2@25=%.1f%% | I: S1=%.1f%% S3=%.1f%% | "
      "J: S1=%.1f%% S3=%.1f%%" % (S0_OK, E_S1_25, E_S2_25, I_S1_25, I_S3_25, J_S1_25, J_S3_25))
assert E_S1_25 < S0_OK, "分析 E 应为「朴素@25 劣于不校准」"
assert E_S2_25 < E_S1_25, "分析 E 应为「双参数 劣于 单参数」"
assert I_S3_25 > I_S1_25 and I_S3_25 > S0_OK, "分析 I 应为「EB 双双占优」"
assert J_S3_25 > J_S1_25, "分析 J 应为「EB 优于朴素」"
# 注意口径：配对差（paired_m25 = +9.05 pp，逐院配对差的均值）≠ 达标率之差（24.3−15.5 = 8.8 pp），
# 图内标注一律用落盘的配对差，与正文 9.05 一致，不要用两条曲线读数现算。
PAIRED_M25 = float(_MSH["paired_m25"])
assert PAIRED_M25 > 0, "配对差应为正"
# 外部：朴素达到 EB@25 水平所需 m（线性插值，取整到 10）
_s1 = MX[MX["strat"] == "S1"].sort_values("m")
J_EQ_M = int(round(float(np.interp(J_S3_25, _s1["ok11"].values, _s1["m"].values)) / 10) * 10)
print("  朴素在 MIMIC 达到 EB@25 水平需 m ≈ %d" % J_EQ_M)

# ---------- 样式 ----------
BLUE, ORG, GRAY, DARK, TEAL = "#0072B2", "#E69F00", "#9AA5B1", "#1B2631", "#CC79A7"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                     "axes.linewidth": 0.8, "axes.unicode_minus": False,
                     "xtick.major.width": 0.8, "ytick.major.width": 0.8, "xtick.labelsize": 7.2,
                     "ytick.labelsize": 7.2})
STY = {"S0": dict(c=GRAY, ls=":", lw=1.3, mk="o", ms=4.2),
       "S1": dict(c=BLUE, ls="-", lw=1.6, mk="o", ms=4.6),
       "S2": dict(c=ORG, ls="-", lw=1.4, mk="s", ms=4.2),
       "S3": dict(c=TEAL, ls="-", lw=2.1, mk="D", ms=4.6)}


def series(ax, df, strats, col):
    for s in strats:
        d = df[df["strat"] == s].sort_values("m")
        st = STY[s]
        ax.plot(d["m"], d[col], color=st["c"], ls=st["ls"], lw=st["lw"], marker=st["mk"],
                ms=st["ms"], zorder=4 if s == "S3" else 3)


def krow(ax, ks, ytxt=-0.055):
    """contributing-centre 数 k 标在 x 轴底行（get_xaxis_transform: x=数据坐标, y=axes 分数）。"""
    for m, k in sorted(ks.items()):
        ax.text(m, ytxt, str(k), ha="center", va="top", fontsize=6.4, color=GRAY,
                transform=ax.get_xaxis_transform())


def panel_letter(ax, s):
    ax.text(-0.135, 1.075, s, transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")


XLAB = "Local patients used for recalibration  ($m$)"
Y_OK = "Recalibration attempts landing\nwithin ±10%  (%)"
Y_ABS = "Residual miscalibration  $|a|$\n(median; band → P90)"

fig, axs = plt.subplots(2, 2, figsize=(7.35, 6.15))
fig.subplots_adjust(left=0.10, right=0.985, top=0.965, bottom=0.085, wspace=0.24, hspace=0.34)
axa, axc = axs[0]          # 顶行：a(左) c(右)
axb, axd = axs[1]          # 底行：b(左) d(右)

# ============ (a) 分析 E：±10% 学习曲线（100 次重抽样；S1 vs S2） ============
series(axa, LC, ["S1", "S2"], "within_09_11")
ref = _v(LC, "S1", 0, "within_09_11")
axa.axhline(ref, color=GRAY, lw=1.0, ls=":")
axa.text(198, ref + 1.5, "no recalibration: %.1f%%" % ref, fontsize=6.8, color=DARK, ha="right",
         bbox=dict(fc="white", ec="none", pad=1.6))
axa.axhline(50, color=DARK, lw=0.8, ls="--", alpha=0.45)
axa.text(198, 51.5, "50% (pre-specified target)", fontsize=6.6, color=DARK, ha="right", alpha=0.75)
ks = {int(r.m): int(r.k) for r in LC[LC["strat"] == "S1"].itertuples()}
krow(axa, ks)
axa.annotate("%.1f%%" % E_S2_25, xy=(25, E_S2_25), xytext=(6, 8.6),
             fontsize=6.8, color="#8A5A00",
             arrowprops=dict(arrowstyle="-", color="#8A5A00", lw=0.6, shrinkA=1, shrinkB=3))
axa.annotate("%.1f%%" % E_S1_25, xy=(25, E_S1_25), xytext=(33, E_S1_25 - 4.6),
             fontsize=6.8, color=BLUE)
axa.set_xlim(-8, 208)
axa.set_ylim(0, 100)
axa.set_ylabel(Y_OK, fontsize=8.4)
axa.legend(["S1  naive, intercept only", "S2  naive, intercept + slope"], fontsize=6.8,
           frameon=False, loc="lower right", handlelength=1.7)
axa.spines[["top", "right"]].set_visible(False)

# ============ (b) 分析 E：残余 |a|（同 (a) 同一抽样设计） ============
series(axb, LC, ["S1", "S2"], "resid_a_med")
for st_, c_ in [("S1", BLUE), ("S2", ORG)]:
    d = LC[LC["strat"] == st_].sort_values("m")
    axb.fill_between(d["m"], d["resid_a_med"], d["resid_a_p90"], color=c_, alpha=0.13, zorder=1)
refa = _v(LC, "S1", 0, "resid_a_med")
axb.axhline(refa, color=GRAY, lw=1.0, ls=":")
axb.text(198, refa + 0.022, "no recalibration: %.2f" % refa, fontsize=6.8, color=DARK, ha="right",
         bbox=dict(fc="white", ec="none", pad=1.6))
axb.annotate("%.2f" % _v(LC, "S1", 25, "resid_a_med"), xy=(25, _v(LC, "S1", 25, "resid_a_med")),
             xytext=(33, _v(LC, "S1", 25, "resid_a_med") + 0.062), fontsize=6.8, color=BLUE)
axb.annotate("%.2f" % _v(LC, "S2", 25, "resid_a_med"), xy=(25, _v(LC, "S2", 25, "resid_a_med")),
             xytext=(33, _v(LC, "S2", 25, "resid_a_med") + 0.062), fontsize=6.8, color="#8A5A00")
axb.set_xlim(-8, 208)
axb.set_ylim(0, max(LC["resid_a_p90"]) * 1.22)
axb.set_xlabel(XLAB, fontsize=8.4)
axb.set_ylabel(Y_ABS, fontsize=8.4)
axb.legend(["S1  naive, intercept only", "S2  naive, intercept + slope"], fontsize=6.8,
           frameon=False, loc="upper right", handlelength=1.7)
axb.spines[["top", "right"]].set_visible(False)

# ============ (c) 分析 I：EB 四策略（200 次配对；LOO 交叉拟合） ============
series(axc, SH, ["S0", "S1", "S2", "S3"], "ok11")
axc.axhline(S0_OK, color=GRAY, lw=1.0, ls=":")
axc.text(198, S0_OK + 1.5, "no recalibration: %.1f%%" % S0_OK, fontsize=6.8, color=DARK, ha="right",
         bbox=dict(fc="white", ec="none", pad=1.6))
axc.axhline(50, color=DARK, lw=0.8, ls="--", alpha=0.45)
axc.text(198, 51.5, "50% (pre-specified target)", fontsize=6.6, color=DARK, ha="right", alpha=0.75)
# m=25 处 S1↔S3 竖向双箭头连线，配对差标注置于其右下方
axc.annotate("", xy=(25, I_S1_25), xytext=(25, I_S3_25),
             arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.0, shrinkA=3.5, shrinkB=3.5))
axc.text(33, 7.5, "+%.2f pp (paired)" % PAIRED_M25, fontsize=7.0, color=TEAL, fontweight="bold")
axc.set_xlim(-8, 208)
axc.set_ylim(0, 100)
axc.set_ylabel(Y_OK, fontsize=8.4)
axc.legend(["S0  no recalibration", "S1  naive, intercept only",
            "S2  naive, intercept + slope", "S3  empirical-Bayes shrinkage"],
           fontsize=6.8, frameon=False, loc="upper left", bbox_to_anchor=(0.012, 0.99),
           handlelength=1.7)
axc.tick_params(labelbottom=False)
axc.spines[["top", "right"]].set_visible(False)

# ============ (d) 分析 J：收缩参数迁移到 MIMIC-IV（200 次配对；参数固定自 eICU） ============
series(axd, MX, ["S0", "S1", "S3"], "ok11")
J_S0 = _v(MX, "S0", 0, "ok11")
axd.axhline(J_S0, color=GRAY, lw=1.0, ls=":")
axd.text(8, J_S0 + 3.2, "no recalibration: %.f%%" % J_S0,
         fontsize=6.8, color=DARK, ha="left",
         bbox=dict(fc="white", ec="none", pad=1.6))
axd.annotate("S3 at $m$ = 25 (%.1f%%)\n≈ S1 at $m$ ≈ %d" % (J_S3_25, J_EQ_M),
             xy=(25, J_S3_25), xytext=(40, 74), fontsize=7.0, color=TEAL, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.9, shrinkB=3))
axd.text(0.03, 0.985, ("fixed from eICU:  $\\bar a$ = %+.3f,  $\\tau^2$ = %.3f\n"
                       "offset to recover  $a^{*}$ = %+.3f"
                       % (MM["abar_eicu"], MM["tau2_eicu"], MM["a_star"])),
         transform=axd.transAxes, fontsize=6.8, va="top", color=DARK,
         bbox=dict(fc="white", ec="#D5D8DC", lw=0.5, pad=2.8))
axd.set_xlim(-10, 408)
axd.set_ylim(0, 100)
axd.set_xlabel(XLAB, fontsize=8.4)
axd.legend(["S0  no recalibration", "S1  naive, intercept only", "S3  empirical-Bayes shrinkage"],
           fontsize=6.8, frameon=False, loc="lower right", handlelength=1.7)
axd.spines[["top", "right"]].set_visible(False)

# 面板标识
panel_letter(axa, "a"); panel_letter(axc, "c"); panel_letter(axb, "b"); panel_letter(axd, "d")

# 顶行 x 轴标签省略（与底行同语义），只在底行标注——但 d 已有；b 在 caption 说明与 d 同轴义
axa.tick_params(labelbottom=False)

for ext, kw in [("png", {"dpi": 600}), ("pdf", {})]:
    fig.savefig(os.path.join(FG, "Fig5_重校准与收缩收益." + ext), bbox_inches="tight", **kw)
plt.close(fig)
print("[saved] Fig5_重校准与收缩收益 (a-d)")
