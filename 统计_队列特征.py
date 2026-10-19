# -*- coding: utf-8 -*-
"""描述性统计：补充表 S1（队列特征）。"""
import io, sys, os, json
import numpy as np, pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
ST = os.path.join(BASE, "09_路B_跨院校准", "03_统计")

hid = pd.read_csv(os.path.join(BASE, "09_路B_跨院校准", "hospital_id_map.csv"),
                  usecols=["stay_id", "hospitalid"])

E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv"), low_memory=False)
E = E.merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()

H0 = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
keep = set(H0[H0["score"] == "SOFA"]["hospital"].tolist())
EC = E[E["hospitalid"].isin(keep)].copy()

M = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_mimiciv.csv"), low_memory=False)
M = M.dropna(subset=["sofa", "age", "male", "hosp_death"]).copy()


def stats_pair(s):
    """同时给出均值(SD) 与 中位数[IQR]，口径由同一行统一决定"""
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return None, None
    return ("%.1f (%.1f)" % (s.mean(), s.std()),
            "%.0f [%.0f–%.0f]" % (s.median(), s.quantile(.25), s.quantile(.75)))


def choose(s_all):
    """以 eICU 全队列为基准决定该行用哪种口径，三列统一"""
    s = pd.to_numeric(s_all, errors="coerce").dropna()
    if s.empty or abs(s.mean() - s.median()) < 0.15 * max(s.std(), 1e-9):
        return 0        # 对称 -> 均值(SD)
    return 1            # 偏态 -> 中位数[IQR]


def build(d, name, choices=None):
    out = {}
    out["n"] = "{:,}".format(len(d))
    out["hospitals"] = str(d["hospitalid"].nunique()) if "hospitalid" in d else "1"
    out["male"] = "%d (%.1f%%)" % (int(d["male"].sum()), 100 * d["male"].mean())
    out["vent"] = ("%d (%.1f%%)" % (int(d["invasive_vent"].sum()), 100 * d["invasive_vent"].mean())
                   if "invasive_vent" in d else "—")
    out["death"] = "%d (%.1f%%)" % (int(d["hosp_death"].sum()), 100 * d["hosp_death"].mean())
    if "icu_death" in d:
        out["icu_death"] = "%d (%.1f%%)" % (int(d["icu_death"].sum()), 100 * d["icu_death"].mean())
    if choices is None:
        choices = {}
        for c in ["age", "cci", "sofa", "oasis", "sapsii"]:
            if c in d.columns:
                choices[c] = choose(d[c])
    for c in ["age", "cci", "sofa", "oasis", "sapsii"]:
        if c in d.columns:
            pair = stats_pair(d[c])
            out[c] = pair[choices.get(c, 0)]
    return out, choices


A, CHOICES = build(E, "eICU all")
B, _ = build(EC, "eICU 103 centres", CHOICES)
C, _ = build(M, "MIMIC-IV", CHOICES)
LBL = {c: ("mean (SD)" if i == 0 else "median [IQR]") for c, i in CHOICES.items()}

KEYS = [("n", "Patients, n"), ("hospitals", "Hospitals, n"),
        ("male", "Male, n (%)"),
        ("age", "Age, years (%s)" % LBL.get("age", "")),
        ("cci", "Comorbidity burden (Charlson, %s)" % LBL.get("cci", "")),
        ("vent", "Invasive ventilation, n (%)"),
        ("sofa", "SOFA score (%s)" % LBL.get("sofa", "")),
        ("oasis", "OASIS score (%s)" % LBL.get("oasis", "")),
        ("sapsii", "SAPS-II score (%s)" % LBL.get("sapsii", "")),
        ("icu_death", "ICU death, n (%)"), ("death", "In-hospital death, n (%)")]

print("=" * 92)
print("  补充表 S1 · 队列特征")
print("=" * 92)
print("  %-52s %-16s %-16s %s" % ("Characteristic", "eICU (all)",
                                  "eICU (103 centres)", "MIMIC-IV"))
print("  " + "-" * 88)
for k, lbl in KEYS:
    print("  %-52s %-16s %-16s %s" % (lbl[:50], A.get(k, "—"), B.get(k, "—"), C.get(k, "—")))

out = dict(eicu_all=A, eicu_103=B, mimiciv=C)
json.dump(out, open(os.path.join(ST, "cohort_characteristics.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("\n  -> 03_统计\\cohort_characteristics.json")
print("=" * 92)