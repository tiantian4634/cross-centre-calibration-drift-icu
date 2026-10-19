# -*- coding: utf-8 -*-
"""合并模型 AUC 的 95% CI —— 按医院整群 bootstrap（cluster bootstrap），numpy 实现。

为何用整群而非按患者重抽样：患者嵌套于医院，医院间校准偏移本身即为本文的研究对象。
把患者当作独立个体重抽样会忽略簇内相关、低估不确定性。
做法：有放回地重抽 187 家医院 → 取其全部患者的索引 → 重新拟合并计算 AUC，
1,000 次的 2.5 / 97.5 百分位即 95% CI。标准化参数沿用原全队列估计，避免重抽样间尺度漂移。
"""
import io, sys, os, json, time
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
ST = os.path.join(BASE, "09_路B_跨院校准", "03_统计")
SEED, B = 20261019, 1000

hid = pd.read_csv(os.path.join(BASE, "09_路B_跨院校准", "hospital_id_map.csv"),
                  usecols=["stay_id", "hospitalid"])
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv"), low_memory=False)
E = E.merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int)
print("[data] 患者 %d，医院 %d" % (len(E), E["hospitalid"].nunique()))
print("[bootstrap] B=%d，按医院整群有放回，seed=%d" % (B, SEED))

OUT = {}
for label, col in [("SOFA", "sofa"), ("OASIS", "oasis"), ("SAPS-II", "sapsii")]:
    t0 = time.time()
    d = E.dropna(subset=[col])
    X0 = d[col].astype(float).values
    mu, sd = X0.mean(), X0.std()
    Y = d["y"].astype(int).values
    h = d["hospitalid"].values

    auc0 = roc_auc_score(Y, LogisticRegression(max_iter=5000, C=1.0)
                         .fit(((X0 - mu) / sd).reshape(-1, 1), Y)
                         .predict_proba(((X0 - mu) / sd).reshape(-1, 1))[:, 1])

    # 按医院预存索引（numpy 数组，避免 pandas 拼接）
    order = np.argsort(h, kind="stable")
    hs = h[order]
    bounds = np.searchsorted(hs, np.unique(hs), side="left")
    ends = np.searchsorted(hs, np.unique(hs), side="right")
    chunks = [order[b:e] for b, e in zip(bounds, ends)]
    k = len(chunks)

    vals = []
    for rep in range(B):
        rng = np.random.default_rng(SEED + rep * 9973)
        pick = rng.integers(0, k, size=k)          # 有放回抽 k 家医院
        idx = np.concatenate([chunks[i] for i in pick])
        yb = Y[idx]
        if yb.min() == yb.max():
            continue
        Xb = ((X0[idx] - mu) / sd).reshape(-1, 1)
        m = LogisticRegression(max_iter=5000, C=1.0).fit(Xb, yb)
        vals.append(roc_auc_score(yb, m.predict_proba(Xb)[:, 1]))

    v = np.asarray(vals)
    lo, hi = np.percentile(v, [2.5, 97.5])
    OUT[label] = dict(auc=round(float(auc0), 4), lo=round(float(lo), 4), hi=round(float(hi), 4),
                      n_boot=int(len(v)), se=round(float(v.std(ddof=1)), 4), k=k)
    print("  %-9s AUC %.3f  95%% CI %.3f–%.3f   (有效重抽样 %d / %d，SE=%.4f，用时 %.0fs)"
          % (label, auc0, lo, hi, len(v), B, v.std(ddof=1), time.time() - t0))

json.dump(OUT, open(os.path.join(ST, "pooled_auc_ci.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("\n  -> 03_统计\\pooled_auc_ci.json")

REF = {"SOFA": 0.7318, "OASIS": 0.7284, "SAPS-II": 0.7609}
print("\n[核对] 与 结果汇总_v1.md 的合并 AUC")
ok = True
for k, v in REF.items():
    got = OUT[k]["auc"]
    same = abs(got - v) < 5e-4
    ok &= same
    print("  %-9s 权威 %.4f / 本次 %.4f  %s" % (k, v, got, "✔" if same else "✘ 差异"))
print("\n" + "=" * 84)
print("  %s" % ("全部一致 ✔ 可直接用于 Table 1" if ok else "✘ 有差异，勿用"))
print("=" * 84)