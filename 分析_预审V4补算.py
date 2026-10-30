# -*- coding: utf-8 -*-
"""预审 V4 意见补算（一轮三件套；只读既有缓存，不改任何主产物/预注册件）：
  1) M2：84 家被排除中心 vs 103 家纳入中心的特征比较（cohort_eicu + hospital_id_map）；
  2) 项8：±20% 宽松带成功率（E 侧从 raw 聚合；I/J 侧读既有 summary 的 ok12 列；
     方法学口径与预注册一致：每次重抽样先跨中心平均，再平均各次）；
  3) M5：103 家中心 SOFA 标准差按规模三分位（检验"大中心病例组合更离散"）。
输出：03_统计/预审V4补算.json + 控制台 markdown 表（供 SI 表格文字化）。
"""
import io, sys, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import numpy as np
import pandas as pd

ST = r"03_统计"
OUT = os.path.join(ST, "预审V4补算.json")
res = {}

E = pd.read_csv(r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\02_数据集\cohort_eicu.csv")
hid = pd.read_csv("hospital_id_map.csv")
E = E.merge(hid, on="stay_id", how="left").dropna(subset=["hospitalid"]).copy()
E["y"] = E["hosp_death"].astype(int)

# ── 1. M2：84 vs 103 ─────────────────────────────────────
H = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
H103 = set(H[H["score"] == "SOFA"]["hospital"])
g_all = E.groupby("hospitalid").agg(
    n=("y", "size"), deaths=("y", "sum"),
    sofa_mean=("sofa", "mean"), sofa_sd=("sofa", "std"),
    oasis_mean=("oasis", "mean"), sapsii_mean=("sapsii", "mean"),
    age_mean=("age", "mean"), male_pct=("male", "mean"),
    vent_pct=("invasive_vent", "mean"), cci_mean=("cci", "mean"),
).reset_index()
g_all["included"] = g_all["hospitalid"].isin(H103)
g_all["mortality"] = g_all["deaths"] / g_all["n"]


def describe(d):
    return dict(k=int(len(d)),
                n_med=float(d["n"].median()), n_iqr=[float(np.percentile(d["n"], 25)), float(np.percentile(d["n"], 75))],
                mort_med=float(d["mortality"].median()),
                sofa_mean=float(np.average(d["sofa_mean"], weights=d["n"])),
                oasis_mean=float(np.average(d["oasis_mean"], weights=d["n"])),
                sapsii_mean=float(np.average(d["sapsii_mean"], weights=d["n"])),
                age_mean=float(np.average(d["age_mean"], weights=d["n"])),
                male_pct=float(np.average(d["male_pct"], weights=d["n"])) * 100,
                vent_pct=float(np.average(d["vent_pct"], weights=d["n"])) * 100,
                sofa_sd_med=float(d["sofa_sd"].median()))


incl = describe(g_all[g_all["included"]])
excl = describe(g_all[~g_all["included"]])
res["M2_country_comparison"] = {"included": incl, "excluded": excl}
print("== M2 103 家纳入 vs %d 家排除 ==" % int(excl["k"]))
for k2 in ["k", "n_med", "n_iqr", "mort_med", "sofa_mean", "age_mean", "vent_pct", "sofa_sd_med"]:
    print(f"  {k2:>12s}: included={incl[k2]} | excluded={excl[k2]}")
print("== 项8 E 侧 ±10%/±20%（复算口径校验 S1,m=25,±10%% 应=15.3）==".replace("%%", "%"))

# ── 2. 项8：±20%（E 侧重聚合；I/J 读既有 summary ok12）─────
L = pd.read_csv(os.path.join(ST, "learning_curve_raw.csv"))
L["ok11"] = ((L["oe"] - 1).abs() <= 0.10).astype(float)
L["ok20"] = ((L["oe"] - 1).abs() <= 0.20).astype(float)
rows = []
check_ok11 = None
for (st_i, m_i), d in L.groupby(["strat", "m"]):
    per_attempt = d.groupby("rep")["ok11"].mean()  # 每次重抽样：先跨中心平均
    per_attempt20 = d.groupby("rep")["ok20"].mean()
    rows.append(dict(strat=str(st_i), m=int(m_i),
                     ok11=round(float(per_attempt.mean() * 100), 1),
                     ok20=round(float(per_attempt20.mean() * 100), 1)))
    if str(st_i) == "S1" and int(m_i) == 25:
        check_ok11 = float(per_attempt.mean() * 100)
res["E_loose_band"] = rows
assert abs(check_ok11 - 15.3) < 0.15, "E ±10% 复算与稿件数字不符: %s" % check_ok11
print("== 项8 E 侧 ±10%/±20%（复算口径校验 S1,m=25,±10%% 应=15.3）==".replace("%%", "%"))
for r5 in rows:
    print("  {strat:>4s} m={m:>3d}: ±10%={ok11:5.1f}%  ±20%={ok20:5.1f}%".format(**r5))

sh = json.load(open(os.path.join(ST, "shrinkage_summary.json"), encoding="utf-8"))["rows"]
mx = json.load(open(os.path.join(ST, "mimic_external_summary.json"), encoding="utf-8"))["rows"]
res["I_loose_band"] = [{"strat": r5["strat"], "m": r5["m"], "ok11": r5["ok11"], "ok20": r5["ok12"]} for r5 in sh if r5["m"] > 0]
res["J_loose_band"] = [{"strat": r5["strat"], "m": r5["m"], "ok11": r5["ok11"], "ok20": r5["ok12"]} for r5 in mx if r5["m"] > 0]
print("I/J ±20% 已从既有 summary 提取（含 S0/S1/S2/S3 × m）")

# ── 3. M5：SOFA 离散度按三分位 ───────────────────────────
sofa_sd = g_all[g_all["included"]][["hospitalid", "sofa_sd"]].copy()
tt = pd.qcut(sofa_sd.join(g_all.set_index("hospitalid")["n"], on="hospitalid")["n"], 3,
             labels=["小", "中", "大"])
d5 = pd.DataFrame({"tert": tt.values, "sd": sofa_sd["sofa_sd"].values,
                   "oasis_sd": g_all.set_index("hospitalid").loc[sofa_sd["hospitalid"], "oasis_mean"].values})
d5 = sofa_sd.assign(tert=tt.values).merge(g_all[["hospitalid", "oasis_mean", "n"]], on="hospitalid")
out5 = []
for t6, g6 in d5.groupby("tert"):
    out5.append(dict(tert=str(t6), k=int(len(g6)),
                     sofa_sd_med=float(g6["sofa_sd"].median()),
                     sofa_sd_mean=float(g6["sofa_sd"].mean())))
res["M5_sofa_dispersion"] = out5
print("== M5 SOFA 标准差按中心规模三分位 ==")
for r5 in out5:
    print("  {tert}: k={k}  SOFA SD 中位={sofa_sd_med:.2f} (均值 {sofa_sd_mean:.2f})".format(**r5))

json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("已写", OUT)
