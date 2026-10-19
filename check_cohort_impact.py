# -*- coding: utf-8 -*-
"""检查：T1 继承队列中「白蛋白/身高/体重全缺失」被排除的病例，有多少其实具备路B 所需的完整变量。
若绝大多数缺 SOFA，则路B 队列无需重建。"""
import io, sys, os
import numpy as np, pandas as pd, duckdb
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
IM = os.path.join(BASE, "01_队列与计数", "intermediate")

sev = pd.read_parquet(os.path.join(IM, "eicu_severity.parquet"))
print(f"[eicu_severity] {len(sev):,} 行 × {sev.shape[1]} 列")
print("  列:", ", ".join(sev.columns.tolist()[:25]))

con = duckdb.connect(r"F:\数据库\MIMIC\mimic-SQL知识库\catalog.duckdb", read_only=True)
p = con.execute('select * from "eicu_crd.eicu_crd".patient').fetchdf()
con.close()
print(f"[patient] {len(p):,} 行；列: " + ", ".join(p.columns.tolist()))

age_num = pd.to_numeric(p["age"].astype(str).str.replace(">", "", regex=False).str.strip(),
                        errors="coerce")
p["age_num"] = np.where(p["age"].astype(str).str.startswith(">"), age_num + 1, age_num)
p = p.sort_values(["uniquepid", "hospitaladmittime24"]).reset_index(drop=True)
p["rn"] = p.groupby("uniquepid").cumcount() + 1

steps, b = {}, p.copy()
steps["all"] = len(b)
b = b[b["rn"] == 1].copy();                      steps["first_stay"] = len(b)
b = b[b["age_num"] >= 65].copy();                steps["age65"] = len(b)
b = b[b["unitdischargeoffset"] >= 1440].copy();  steps["los24h"] = len(b)
b = b[b["unittype"].isin(["MICU", "Med-Surg ICU"])].copy(); steps["unit_type"] = len(b)
hdt = b["hospitaldischargeoffset"] - b["hospitaladmitoffset"]
m24 = ((b["hospitaldischargestatus"] == "expired") & (hdt <= 1440))
steps["excl_death24h"] = int(m24.sum()); b = b[~m24].copy()
bad = ~b["hospitaldischargestatus"].isin(["expired", "alive"])
steps["excl_missing_outcome"] = int(bad.sum()); b = b[~bad].copy()
steps["after_outcome"] = len(b)

# 合入 SOFA 表，看这些候选里有多少具备路B 所需变量
key = "patientunitstayid" if "patientunitstayid" in sev.columns else sev.columns[0]
soc = [c for c in sev.columns if c.lower() in ("sofa", "oasis", "sapsii", "age", "male")]
m = b.merge(sev[[key] + soc], on=key, how="left", suffixes=("", "_sev"))
have_sofa = m[soc[0]].notna().sum() if soc else 0
print(f"\n[路B 口径] 结局可判定者 = {steps['after_outcome']:,}")
print(f"  其中具备完整 SOFA 的 = {have_sofa:,}")
print(f"  → 若再排除 SOFA 缺失，路B 分析队列应为 {have_sofa:,}，"
      f"而既有 T1 队列为 30,796，差 {have_sofa-30796:+,}")
print(f"  T1 队列额外排除了「白蛋白/身高/体重全缺失」141 例"
      f"（占 {141/30796*100:.2f}%），路B 未使用这些变量。")
print("\n各步计数：", steps)
