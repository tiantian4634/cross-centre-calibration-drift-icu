# -*- coding: utf-8 -*-
"""诊断：多水平 logistic 的 τ² 为何与两阶段 meta 分析差近 2 倍？
分别用 fit_map / fit_vb × 多个先验强度，并检查是否真收敛。"""
import io, sys, os, json, warnings
import numpy as np, pandas as pd
from scipy.special import expit, logit
import statsmodels.api as sm
import statsmodels.genmod.bayes_mixed_glm as bmg

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
print(f"[data] n={len(E):,}；k={E['hosp'].nunique()}")

REF = 0.1312   # DL τ²（两阶段 meta 分析）
print(f"[参照] 两阶段 meta 分析 τ²(DL) = {REF:.4f}\n")

rows = []
for vcp in [0.5, 1.0, 2.0, 100.0]:
    for meth in ["map", "vb"]:
        try:
            mdl = sm.BinomialBayesMixedGLM.from_formula(
                "y ~ lp", {"hosp": "0 + C(hosp)"}, E, fe_p=2.0, vcp_p=vcp)
            if meth == "map":
                f = mdl.fit_map(method="BFGS", minim_opts=dict(maxiter=3000))
            else:
                f = mdl.fit_vb(minim_opts=dict(maxiter=3000))
            t2 = float(np.exp(f.vcp_mean[0]))
            se = float(np.exp(f.vcp_sd[0]) * t2) if hasattr(f, "vcp_sd") else np.nan
            rows.append(dict(vcp_p=vcp, method=meth.upper(), tau2=t2,
                             sd_log=se, loglike=float(np.max(f.llf)) if hasattr(f, "llf") else np.nan,
                             b_fe=float(f.fe_mean[1]), a_fe=float(f.fe_mean[0]),
                             rel=100 * (t2 - REF) / REF))
            print(f"  vcp_p={vcp:<6} {meth.upper():<4} τ² = {t2:.4f}  (vs DL {REF:.4f}  {rows[-1]['rel']:+.1f}%)"
                  f"   b={f.fe_mean[1]:.4f}  a={f.fe_mean[0]:+.4f}")
        except Exception as e:
            print(f"  vcp_p={vcp:<6} {meth.upper():<4} FAILED: {type(e).__name__}: {e}")

# ---------- 独立核对：直接写边际似然做 REML/ML 的随机截距 logistic ----------
print("\n" + "=" * 78)
print("### 独立核对：手工边际似然（高斯-埃尔米特求积）估计随机截距方差")
print("=" * 78)
import numpy.polynomial.hermite_e as _he
from scipy.optimize import minimize_scalar

g = E.groupby("hosp")
groups = [(gy["lp"].values, gy["y"].values) for _, gy in g]
NQ = 25
nodes, weights = _he.hermegauss(NQ)          # 标准正态（概率学家 Hermite）
wgt = weights / np.sqrt(2 * np.pi)
nodes = nodes * np.sqrt(2.0)


def negll(tau2, groups, fixed_a=False):
    """Marginal (integrated) log-likelihood with a shared slope b and random intercept ~N(0,tau2)."""
    sd = np.sqrt(max(tau2, 1e-12))
    u = nodes * sd
    tot = 0.0
    for lp, y in groups:
        eta_b = np.outer(u, np.ones(len(lp))) + lp[None, :] * b_opt   # u_j + b*lp
        p = expit(eta_b)
        ll_node = (y[None, :] * np.log(np.clip(p, 1e-12, 1)) +
                   (1 - y[None, :]) * np.log(np.clip(1 - p, 1e-12, 1))).sum(1)
        tot += np.log(np.sum(wgt * np.exp(ll_node - ll_node.max()))) + ll_node.max()
    return -tot


b_opt = 1.0
# 先在 tau2 上做剖面对 b 的优化
def negll2(t2):
    global b_opt
    r = minimize_scalar(lambda b: (lambda t: t)(negll_with_b(t2, b)),
                        bounds=(0.2, 3.0), method="bounded")
    return r.fun


def negll_with_b(t2, b):
    global b_opt
    saved = b_opt; b_opt = b
    v = negll(t2, groups)
    b_opt = saved
    return v


r = minimize_scalar(lambda t: negll_with_b(t, 1.03), bounds=(1e-4, 3.0), method="bounded",
                    options=dict(xatol=1e-6))
t2_ml = float(r.x)
print(f"  边际极大似然（固定 b=1.03）：τ² = **{t2_ml:.4f}**  (vs DL {REF:.4f}  {100*(t2_ml-REF)/REF:+.1f}%)")
r2 = minimize_scalar(lambda b: negll_with_b(REF, b), bounds=(0.2, 3.0), method="bounded")
print(f"  在 τ² 固定为 DL 值时的最优 b = {r2.x:.4f}")
print(f"  （边际似然 vs MAP/VB：后者含先验，前者纯似然）")

json.dump(rows, open(os.path.join(ST, "multilevel_diagnostic.json"), "w", encoding="utf-8"),
          indent=2)
print("[done]")
