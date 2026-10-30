# 表 1–表 3 —— Scientific Reports 投稿版

> **Sci Rep 硬性要求**
> - 表格须在**稿件文件内、可编辑格式**，不得作为图片上传
> - **每张主表不得超过一页**
> - **不支持彩色表格**（黑白可读）
> - 含统计分析的表须**在表注中说明误差与范围的统计处理**
> - 表格与图合计（display items）上限 **8 个** → 本稿：表1（正文）+ 表S1、表S2（补充）+ 图1–7 + 补充图S1–S3
> - 表格须置于参考文献**之前**的正文内（图注与图则在参考文献之后）
>
> 以下 Markdown 表格可直接粘贴进 Word 并转为「插入表格」；粘贴后请确认**无单元格底色**。

---

## Table 1（正文）—— 三评分的跨中心校准漂移

**Table 1. Between-centre variation in discrimination and calibration across 103 intensive-care
units, by severity score**

| | SOFA | OASIS | SAPS-II |
|---|---|---|---|
| Hospitals included, *k* | 103 | 103 | 103 |
| Pooled model AUC (95% CI) | 0.732 (0.720–0.745) | 0.728 (0.715–0.741) | 0.761 (0.751–0.771) |
| Per-centre AUC, 10th / median / 90th percentile | 0.649 / 0.738 / 0.812 | 0.666 / 0.729 / 0.813 | 0.683 / 0.762 / 0.844 |
| Between-centre variance (τ²) | 0.131 | 0.165 | 0.109 |
| Between-centre heterogeneity, I² (%) | 75.4 | 79.8 | 70.4 |
| Observed-to-expected mortality ratio, 10th / median / 90th percentile | 0.69 / 0.96 / 1.54 | 0.71 / 1.03 / 1.57 | 0.69 / 1.02 / 1.49 |
| Calibration slope, 10th / median / 90th percentile | 0.720 / 1.088 / 1.639 | 0.734 / 1.104 / 1.681 | 0.753 / 1.039 / 1.509 |

**Table 1 legend.** Each score was fitted as a single-score pooled logistic model across the full
eICU-CRD cohort (30,796 patients, 3,901 in-hospital deaths), and the calibration-in-the-large offset
and calibration slope were then derived separately in each of the 103 hospitals meeting the
pre-specified eligibility criterion of ≥ 100 patients and ≥ 10 in-hospital deaths. AUC, area under
the receiver operating characteristic curve; O/E, observed-to-expected mortality ratio; τ²,
between-centre variance estimated by the DerSimonian–Laird method; I², proportion of total variation
attributable to between-centre heterogeneity. **95% confidence intervals for the pooled AUC were
obtained by cluster bootstrap**, resampling the 187 hospitals with replacement and taking all of each
sampled hospital's patients (1,000 replicates; percentile interval; random seed 20261019). The
standardisation parameters of the pooled model were held fixed across replicates. Percentiles in the
other rows are the 10th and 90th percentiles across hospitals and are **measures of spread, not
confidence intervals**. **No hypothesis test was performed for any entry in this table**; the values
are descriptive estimates. The narrow confidence intervals around the pooled AUC (width ≈ 0.025)
contrast with the 2.2-fold spread in the observed-to-expected ratio, which is the comparison this
table is intended to make.

> **一页可行性**：8 行 × 4 列，实际排版约 1/3 页。✔

---

## Supplementary Table S1 —— 队列特征

**Supplementary Table S1. Cohort characteristics**

| Characteristic | eICU-CRD (all) | eICU-CRD (103 centres) | MIMIC-IV |
|---|---|---|---|
| Patients, n | 30,796 | 26,436 | 8,579 |
| Hospitals, n | 187 | 103 | 1 |
| Male, n (%) | 15,538 (50.5) | 13,396 (50.7) | 4,338 (50.6) |
| Age, years, mean (SD) | 77.0 (7.7) | 76.9 (7.7) | 77.7 (8.3) |
| Charlson comorbidity index, mean (SD) | 0.9 (1.3) | 0.9 (1.3) | 3.5 (2.5) |
| **Missing data, n (%)** | | | |
| └ Severity scores (SOFA / OASIS / SAPS-II) | 0 (0) | 0 (0) | 0 (0) |
| └ Age, sex, invasive ventilation | 0 (0) | 0 (0) | 0 (0) |
| └ In-hospital death (outcome) | 0 (0) | 0 (0) | 0 (0) |
| └ Charlson comorbidity index | 3,560 (11.6) | 2,807 (10.6) | 3 (0.04) |
| Invasive ventilation, n (%) | 6,683 (21.7) | 6,134 (23.2) | 2,062 (24.0) |
| SOFA score, mean (SD) | 4.3 (3.2) | 4.4 (3.3) | 5.5 (3.5) |
| OASIS score, median [IQR] | 27 [22–34] | 27 [22–35] | 33 [28–39] |
| SAPS-II score, median [IQR] | 35 [28–45] | 35 [28–45] | 41 [34–51] |
| ICU death, n (%) | 2,325 (7.5) | 2,094 (7.9) | 1,014 (11.8) |
| In-hospital death, n (%) | 3,901 (12.7) | 3,486 (13.2) | 1,654 (19.3) |

**Supplementary Table S1 legend.** Continuous variables are summarised as mean (SD) where the
distribution was approximately symmetric in the full eICU-CRD cohort and as median [interquartile
range] otherwise; the same summary is used for that row in all three columns. Percentages are
column percentages and may not sum to 100 because of rounding. eICU-CRD (103 centres) is the subset
of patients contributing to the centre-level analyses. **Missing data** are reported for every
analysis variable; all variables except the Charlson comorbidity index are complete, so no imputation
was performed. Comorbidity index enters only the descriptive case-mix analysis, which uses complete
cases; every other analysis uses a set with no missing values.

> **⚠️ 需在正文局限性中配套说明的一点**：MIMIC-IV 的 Charlson 指数均值 3.5 明显高于 eICU 的 0.9。
> 两个数据库的合并症**编码完整性不同**（MIMIC-IV 基于更完整的住院 ICD 编码），
> 属**记录差异**而非真实的病例组合差异。**分析 J 只使用 SOFA 单评分模型，不使用合并症变量，
> 因此该差异不影响任何结论**，但须在局限性中如实写出，否则会被追问。

---

## Supplementary Table S2 —— τ² 的四框架估计

**Supplementary Table S2. Between-centre variance estimated under four frameworks**

| Estimation framework | τ² | I², % | Pooled mean (ā) | Relative difference from two-stage median |
|---|---|---|---|---|
| DerSimonian–Laird (two-stage) | 0.1312 | 75.35 | +0.030 | — |
| Paule–Mandel (two-stage) | 0.1261 | 75.35 | +0.0304 | −3.9% |
| REML (two-stage) | 0.1299 | 75.35 | +0.0301 | −1.0% |
| One-stage multilevel logistic | 0.0648 | — | +0.0745 | **−50.1%** |

**Supplementary Table S2 legend.** Two-stage estimates were obtained by random-effects
meta-analysis of the 103 hospital-level calibration offsets. The one-stage estimate was obtained by
fitting a random-intercept logistic regression to patient-level data (26,436 patients, 103 groups)
by maximum *a posteriori* estimation; τ² is the square of the estimated random-effect standard
deviation. Maximum *a posteriori* estimation of a variance component is sensitive to initialisation;
repeated fits give standard deviations of 0.247–0.255 (τ² 0.061–0.065), and an independent
marginal-likelihood calculation gave τ² = 0.0706. Pooled mean ā is reported with random-effects
weights for the two-stage frameworks. **The pre-specified criterion** required the relative range
across the three two-stage estimators to be < 25% (observed 3.9%, met) **and** the one-stage
estimate to lie within 50% of their median (observed −50.1%, **not met**); the disagreement is
reported as a negative finding.

---

## Supplementary Table S3 —— 主结论对 τ² 取值的敏感性

**Supplementary Table S3. Sensitivity of the empirical-Bayes result to the choice of between-centre variance**

| Local patients (*m*) | τ² = 0.1312 (DL) | τ² = 0.0706 (marginal likelihood) | τ² = 0.0648 (multilevel) |
|---|---|---|---|
| 25 | 15.5% → **24.3%** (+9.1, P = 2.3 × 10⁻¹¹³) | 15.5% → **21.9%** (+6.7, P = 2.7 × 10⁻⁶⁴) | 15.5% → **21.7%** (+6.5, P = 1.3 × 10⁻⁶⁰) |
| 50 | 19.7% → **26.4%** (+6.7, P = 1.4 × 10⁻⁶¹) | 19.7% → **24.3%** (+4.6, P = 1.6 × 10⁻²⁹) | 19.7% → **23.8%** (+4.2, P = 1.4 × 10⁻²⁴) |
| 100 | 25.7% → **30.4%** (+4.7, P = 1.2 × 10⁻¹⁸) | 25.7% → **27.7%** (+2.0, P = 4.6 × 10⁻⁴) | 25.7% → **27.6%** (+1.9, P = 0.001) |
| 200 | 32.3% → **34.4%** (+2.0, P = 0.035) | 32.3% → **32.6%** (+0.2, P = 0.832) | 32.3% → **32.5%** (+0.2, P = 0.889) |

**Supplementary Table S3 legend.** Each cell gives the success rate of naive local recalibration →
that of empirical-Bayes shrinkage, with the difference in percentage points and the two-sided
Wilcoxon signed-rank *P* value across paired (hospital, replicate) observations; α = 0.05. Two
hundred resampling attempts were used per cell, on the same draws for all three values of *τ²*, so
that the columns differ only in the variance used for shrinkage. The three candidate values were
chosen to span the range produced by the estimation frameworks compared in Supplementary Table S2:
0.1312 (DerSimonian–Laird, used in all primary analyses), 0.0706 (marginal likelihood) and 0.0648
(one-stage multilevel). **The pre-specified criterion** — that shrinkage exceed naive recalibration
at *m* = 25 — was met under all three values (all *P* < 10⁻⁵⁹). The magnitude of the advantage
depends on *τ²* and the advantage is not statistically detectable at *m* = 200 for the two smaller
values, which is why the strategy is described as one for small local samples rather than a general
replacement for naive estimation.

---

## Supplementary Table S4 —— 中心级资格标准的中心构成比较（post-hoc，exploratory）

**Supplementary Table S4. Characteristics of the eligible (103) and excluded (84) centres, all 187 hospitals**

| Centre group | Centres, *k* | Patients per centre, median (IQR) | Mortality, median | SOFA, mean | Ventilated, % |
|---|---|---|---|---|---|
| Eligible (≥100 patients and ≥10 deaths) | 103 | 224 (166–306) | 12.7% | 4.39 | 23.2 |
| Excluded (below that threshold) | 84 | 47 (19–78) | 9.0% | 3.48 | 12.6 |

**Supplementary Table S4 legend.** All 187 hospitals that contribute patients to the pooled model were
characterised from the analysis cohort; means are patient-weighted within each group of centres. The
excluded 44.9% of centres are smaller and less severely ill on average; how their calibration offsets
behave cannot be estimated within the prespecified centre-level framework, and the direction of any
resulting difference in the between-centre variance is discussed in the main text.

---

## Supplementary Table S5 —— ±20% 宽松带下的成功率（预注册口径的次要指标；post-hoc 补报）

**Supplementary Table S5. Success rates under the prespecified ±20% band (|O/E − 1| ≤ 0.20), secondary measure**

| Analysis | Strategy | *m* = 25 | *m* = 50 | *m* = 100 | *m* = 200 | *m* = 400 |
|---|---|---|---|---|---|---|
| E (learning curve, naive) | S1 | 30.6% | 39.3% | 48.9% | 62.8% | — |
| E (learning curve, naive) | S2 | 30.2% | 38.7% | 48.8% | 62.1% | — |
| I (shrinkage, eICU) | S1 | 31.0% | 38.3% | 48.4% | 59.9% | — |
| I (shrinkage, eICU) | S2 | 30.4% | 38.2% | 48.2% | 59.8% | — |
| I (shrinkage, eICU) | S3 | 47.9% | 51.0% | 56.4% | 61.4% | — |
| J (transfer, MIMIC-IV) | S1 | 42.0% | 49.5% | 71.5% | 84.5% | 97.0% |
| J (transfer, MIMIC-IV) | S3 | 82.0% | 80.0% | 85.0% | 89.0% | 98.0% |

**Supplementary Table S5 legend.** The prespecified 50% target applies only to the ±10% band; this
table reports the ±20% secondary band named in the prespecified analysis plan and Methods. Under
±20%, naive recalibration at 25 patients remains worse than no recalibration on eICU (30.6% versus
41.7%), the empirical-Bayes advantage is undiminished (47.9% versus 31.0%; transfer 82.0% versus
42.0%), and rates converge at larger *m* as in the primary band. The no-recalibration benchmark is a
centre-level residual and is independent of *m*: 21.4% (±10%) and 41.7% (±20%).

---

## 装配时的核对

- [ ] 三张表均在 Word 中为**可编辑表格**（非图片）
- [ ] 无单元格底色、无彩色文字
- [ ] 每张表配表注（legend），含统计处理说明
- [ ] 表格位于参考文献**之前**
- [ ] 主表（Table 1）实际排版**不超过一页**
- [ ] display items 合计 = 7 图 + 1 主表 = **8**，补充另计