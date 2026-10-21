# -*- coding: utf-8 -*-
"""分析 E 的中心级过滤器敏感性检查（投稿前质量审查补充）。

背景：预注册（学习曲线_预注册.md）声明中心级过滤 n ≥ 200；实际流水线对全部 103 家
 centre-eligible 医院仅施加 n ≥ 2m 规则，因此 m=0/25/50 三个单元包含 44 家
 100–199 名患者的医院（m≥100 时 n≥2m 自动蕴含 n≥200，单元集与声明一致）。

本脚本对「严格按计划的 n≥200 过滤」重算各单元 ±10%/±20% 达标率，与已报告值对照，
固定 learning_curve_raw.csv 与 hospital_level.csv 无需数据库凭据即可复现。
"""
import io, sys, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
raw = pd.read_csv(os.path.join(HERE, "03_统计", "learning_curve_raw.csv"))
hl = pd.read_csv(os.path.join(HERE, "hospital_level.csv")).set_index("hospital")["n"]
raw["n"] = raw["hospital"].map(hl)
assert raw["n"].notna().all(), "learning-curve 医院必须都能在 hospital_level.csv 找到 n"

small = int((raw.groupby("hospital")["n"].first() < 200).sum())
out = {"centre_filter_declared": "n>=200", "rule_applied": "n>=2m over 103 eligible centres",
       "centres_100_to_199": small, "S1": {}, "S2": {}}

for strat in ["S1", "S2"]:
    for m in [0, 25, 50, 100, 200]:
        cell = raw[(raw.strat == strat) & (raw.m == m)]
        big = cell[cell["n"] >= 200]
        r = {"k_all": int(cell.hospital.nunique()), "k_n200": int(big.hospital.nunique())}
        for site, df in [("all", cell), ("n>=200", big)]:
            for tol, key in [(0.10, "ok10"), (0.20, "ok20")]:
                r[key + "_" + site] = round(float(((df["oe"] - 1).abs() <= tol).mean() * 100), 1)
        r["delta_ok10"] = round(r["ok10_all"] - r["ok10_n>=200"], 1)
        out[strat][str(m)] = r

os.makedirs(os.path.join(HERE, "03_统计"), exist_ok=True)
with open(os.path.join(HERE, "03_统计", "learning_curve_filter_sensitivity.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"100–199 患者的中心数: {small}")
print(f"{'m':>4} | {'k全/严格':>8} | S1 ±10% 全体→严格 | Δ | S2 ±10% 全体→严格 | Δ")
for strat in ["S1", "S2"]:
    for m in [0, 25, 50, 100, 200]:
        r = out[strat][str(m)]
        print(f"{m:>4} | {r['k_all']:>3}/{r['k_n200']:<4} | {r['ok10_all']:>5.1f}→{r['ok10_n>=200']:<5.1f} | {r['delta_ok10']:+.1f}")
