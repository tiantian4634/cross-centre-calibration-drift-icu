# -*- coding: utf-8 -*-
"""路B 补充字段提取 + 时间漂移可行性（只读；结果缓存，后续分析不再连库）。"""
import io, sys, os
import duckdb
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
SRCDIR = os.path.join(BASE, "09_路B_跨院校准")
out = os.path.join(SRCDIR, "eicu_hospital_context.csv")

con = duckdb.connect(r"F:\数据库\MIMIC\mimic-SQL知识库\catalog.duckdb", read_only=True)
df = con.execute('''
  select patientunitstayid as stay_id, hospitalid,
         hospitaldischargeyear, unittype, wardid, hospitaladmitsource,
         ethnicity, uniquepid, unitstaytype
  from "eicu_crd.eicu_crd".patient
''').fetchdf()
con.close()
df.to_csv(out, index=False)
print(f"[save] {len(df):,} 行 -> {out}")

# 队列内年份分布
import pandas as pd
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv"))
E = E.merge(df, on="stay_id", how="left")
print(f"\n[eICU 队列] {len(E):,} 例；hospitaldischargeyear 缺失 {E['hospitaldischargeyear'].isna().sum():,}")
print("\n=== 年份分布 ===")
vc = E["hospitaldischargeyear"].value_counts().sort_index()
for y, n in vc.items():
    print(f"  {int(y)}: {n:>7,}")
print(f"\n=== 年份 × 每院例数（判断时间漂移是否有足够样本）===")
g = E.groupby("hospitaldischargeyear")["hospitalid"].agg(["count", "nunique"])
print(g.to_string())
print(f"\n=== 院内跨年覆盖：每家医院有几年的数据 ===")
yy = E.groupby("hospitalid")["hospitaldischargeyear"].nunique()
for k, v in yy.value_counts().sort_index().items():
    print(f"  {int(k)} 年: {v:>4} 家医院")
print(f"\n=== ICU 类型分布 ===")
print(E["unittype"].value_counts().to_string())
