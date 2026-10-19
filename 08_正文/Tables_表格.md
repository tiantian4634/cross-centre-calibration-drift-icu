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
| Pooled model AUC | 0.732 | 0.728 | 0.761 |
| Per-centre AUC, 10th / median / 90th percentile | 0.649 / 0.738 / 0.812 | 0.666 / 0.729 / 0.813 | 0.683 / 0.762 / 0.844 |
| Between-centre variance (τ²) | 0.131 | 0.165 | 0.109 |
| Between-centre heterogeneity (I²), % | 75.4 | 79.8 | 70.4 |
| Observed-to-expected mortality ratio, 10th / median / 90th percentile | 0.69 / 0.96 / 1.54 | 0.71 / 1.03 / 1.57 | 0.69 / 1.02 / 1.49 |
| Calibration slope, 10th / median / 90th percentile | 0.720 / 1.088 / 1.639 | 0.734 / 1.104 / 1.681 | 0.753 / 1.039 / 1.509 |

**Table 1 legend.** Each score was fitted as a single-score pooled logistic model across the full
eICU-CRD cohort (30,796 patients, 3,901 in-hospital deaths), and the calibration-in-the-large offset
and calibration slope were then derived separately in each of the 103 hospitals meeting the
pre-specified eligibility criterion of ≥ 100 patients and ≥ 10 in-hospital deaths. AUC, area under the
receiver operating characteristic curve; O/E, observed-to-expected mortality ratio; τ², between-centre
variance estimated by the DerSimonian–Laird method; I², proportion of total variation attributable to
between-centre heterogeneity. Percentiles are the 10th and 90th percentiles across hospitals and are
**measures of spread, not confidence intervals**. **No hypothesis test was performed for any entry in
this table**; the values are descriptive estimates.

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
| Invasive ventilation, n (%) | 6,683 (21.7) | 6,134 (23.2) | 2,062 (24.0) |
| SOFA score, mean (SD) | 4.3 (3.2) | 4.4 (3.3) | 5.5 (3.5) |
| OASIS score, median [IQR] | 27 [22–34] | 27 [22–35] | 33 [28–39] |
| SAPS-II score, median [IQR] | 35 [28–45] | 35 [28–45] | 41 [34–51] |
| ICU death, n (%) | 2,325 (7.5) | 2,094 (7.9) | 1,014 (11.8) |
| In-hospital death, n (%) | 3,901 (12.7) | 3,486 (13.2) | 1,654 (19.3) |

**Supplementary Table S1 legend.** Continuous variables are summarised as mean (SD) where the
distribution was approximately symmetric in the full eICU-CRD cohort and as median [interquartile
range] otherwise; the same summary is used for that row in all three columns. Percentages are column
percentages and may not sum to 100 because of rounding. eICU-CRD (103 centres) is the subset of
patients contributing to the centre-level analyses.

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

## 装配时的核对

- [ ] 三张表均在 Word 中为**可编辑表格**（非图片）
- [ ] 无单元格底色、无彩色文字
- [ ] 每张表配表注（legend），含统计处理说明
- [ ] 表格位于参考文献**之前**
- [ ] 主表（Table 1）实际排版**不超过一页**
- [ ] display items 合计 = 7 图 + 1 主表 = **8**，补充另计