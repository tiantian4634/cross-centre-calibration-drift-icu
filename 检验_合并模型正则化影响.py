import io, sys, os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


def round_up_1dp(x):
    """保留一位小数的保守上界：3.62 -> 3.7"""
    import math
    return math.ceil(round(x, 6) * 10) / 10

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
hid = pd.read_csv(os.path.join(BASE, "09_路B_跨院校准", "hospital_id_map.csv"),
                  usecols=["stay_id", "hospitalid"])
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv")).merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int)

MODELS = [
    ("M1 SOFA", ["sofa"]),
    ("M1 OASIS", ["oasis"]),
    ("M1 SAPS-II", ["sapsii"]),
    ("M2 SOFA+age+sex", ["sofa", "age", "male"]),
    ("M3 +cci+vent", ["sofa", "age", "male", "cci", "invasive_vent"]),
    ("M3 OASIS full", ["oasis", "age", "male", "cci", "invasive_vent"]),
    ("M3 SAPS-II full", ["sapsii", "age", "male", "cci", "invasive_vent"]),
]

print("=" * 96)
print("  L2 正则化影响：全部合并模型")
print("=" * 96)
print("  %-18s %7s  %-13s %-13s  %-11s  %s"
      % ("模型", "n", "AUC(C=1.0)", "AUC(C=1e12)", "ΔAUC", "概率最大绝对差"))
gmax_p, gmax_c, gmax_auc, rows = 0.0, 0.0, 0.0, 0
for name, cols in MODELS:
    d = E.dropna(subset=cols + ["y"]).copy()
    if len(d) == 0 or d["y"].nunique() < 2:
        print("  %-18s 跳过（数据不足）" % name); continue
    X = d[cols].astype(float).values
    mu, sd = X.mean(0), np.where(X.std(0) == 0, 1, X.std(0))
    Xs = (X - mu) / sd
    y = d["y"].values
    pen = LogisticRegression(max_iter=5000, C=1.0).fit(Xs, y)
    unp = LogisticRegression(max_iter=5000, C=1e12).fit(Xs, y)
    a = pen.predict_proba(Xs)[:, 1]
    b = unp.predict_proba(Xs)[:, 1]
    ap, bp = roc_auc_score(y, a), roc_auc_score(y, b)
    dp = float(np.abs(a - b).max())
    dc = float(np.abs(pen.coef_[0] - unp.coef_[0]).max())
    gmax_p = max(gmax_p, dp); gmax_c = max(gmax_c, dc); gmax_auc = max(gmax_auc, abs(ap - bp))
    rows += 1
    print("  %-18s %7d  %-13.6f %-13.6f  %-11.1e  %.3e"
          % (name, len(d), ap, bp, abs(ap - bp), dp))

print("\n" + "=" * 96)
print("  汇总（%d 个模型）" % rows)
print("=" * 96)
print("  ΔAUC 最大           : %.3e  （= %.1f × 10⁻⁶）" % (gmax_auc, gmax_auc * 1e6))
print("  概率最大绝对差       : %.3e  （= %.1f × 10⁻⁴）" % (gmax_p, gmax_p * 1e4))
print("  系数最大绝对差       : %.3e  （= %.1f × 10⁻⁴）" % (gmax_c, gmax_c * 1e4))
print()
print("  → 建议写法：概率差上界 %.1f × 10⁻⁴；ΔAUC 上界 %.1f × 10⁻⁶"
      % (round_up_1dp(gmax_p * 1e4), round_up_1dp(gmax_auc * 1e6)))