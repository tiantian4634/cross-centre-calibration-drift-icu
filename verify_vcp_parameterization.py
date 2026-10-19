# -*- coding: utf-8 -*-
"""决定性验证：statsmodels BinomialBayesMixedGLM 的 vcp_mean 到底是 log(SD) 还是 log(variance)？
方法：与拟合出的随机效应的经验 SD 直接比对。"""
import io, sys, os, warnings
import numpy as np, pandas as pd
from scipy.special import logit
import statsmodels.api as sm
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
warnings.filterwarnings("ignore")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图"
SRCDIR = os.path.join(BASE, "09_路B_跨院校准"); ST = os.path.join(SRCDIR, "03_统计")
H = pd.read_csv(os.path.join(ST, "hospital_level_三评分.csv"))
H = H[H["score"] == "SOFA"]
hid = pd.read_csv(os.path.join(SRCDIR, "hospital_id_map.csv"))
E = pd.read_csv(os.path.join(BASE, "02_数据集", "cohort_eicu.csv")).merge(hid, on="stay_id", how="left")
E = E.dropna(subset=["hospitalid", "sofa", "age", "male", "hosp_death"]).copy()
E["y"] = E["hosp_death"].astype(int)
from sklearn.linear_model import LogisticRegression
mu, sd = E["sofa"].mean(), E["sofa"].std()
mp = LogisticRegression(max_iter=5000, C=1.0).fit(((E[["sofa"]].values - mu) / sd), E["y"].values)
E["lp"] = logit(np.clip(mp.predict_proba((E[["sofa"]].values - mu) / sd)[:, 1], 1e-8, 1 - 1e-8))
E["hosp"] = E["hospitalid"].astype(int)
E = E[E["hosp"].isin(set(H["hospital"].astype(int).tolist()))].copy()

mdl = sm.BinomialBayesMixedGLM.from_formula("y ~ lp", {"hosp": "0 + C(hosp)"}, E,
                                            fe_p=2.0, vcp_p=100.0)
f = mdl.fit_map(method="BFGS", minim_opts=dict(maxiter=3000))

vcp_raw = f.vcp_mean                       # 模型内部参数
re = f.random_effects                      # 每组随机效应
print("=== 拟合结果 ===")
print(f"  vcp_mean (模型内部参数)      = {vcp_raw}")
print(f"  exp(vcp_mean)                = {np.exp(vcp_raw[0]):.4f}")
print(f"  随机效应个数                = {len(re)}")
vals = np.array(list(re.values()))
print(f"  随机效应【经验 SD】          = {vals.std(ddof=1):.4f}")
print(f"  随机效应【经验方差】         = {vals.var(ddof=1):.4f}")
print()
expv = float(np.exp(vcp_raw[0]))
print("=== 判定 ===")
print(f"  exp(vcp_mean) = {expv:.4f}  vs  经验 SD = {vals.std(ddof=1):.4f}"
      f"  → {'✅ 匹配 SD：vcp_mean = log(SD)' if abs(expv - vals.std(ddof=1)) < 0.05 else '不匹配 SD'}")
print(f"  exp(vcp_mean) = {expv:.4f}  vs  经验方差 = {vals.var(ddof=1):.4f}"
      f"  → {'✅ 匹配方差：vcp_mean = log(variance)' if abs(expv - vals.var(ddof=1)) < 0.05 else '不匹配方差'}")
print()
print("=== 结论换算 ===")
print(f"  若 exp(vcp_mean)=SD：τ² = SD² = **{expv**2:.4f}**")
print(f"  两阶段 meta 分析 τ²(DL) = 0.1312；手工边际似然 ML = 0.0706")
print(f"  → 正确的多水平 τ² 与哪者接近？")
print(f"      vs DL(0.1312)：{100*(expv**2-0.1312)/0.1312:+.1f}%")
print(f"      vs ML(0.0706)：{100*(expv**2-0.0706)/0.0706:+.1f}%")
