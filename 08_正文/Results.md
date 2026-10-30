# Results —— Scientific Reports 投稿版

> **图号已按投稿方案重编**：正文 5 张连续编号（Fig. 1–5，其中 Fig.5 为 a–d 合并面板），补充材料 S1–S3。
>
> | 投稿编号 | 内容 | 文件 | 去向 |
> |---|---|---|---|
> | **Fig. 1** | 两库筛选流程图 | `Fig1_两库筛选流程图` | 正文 |
> | **Fig. 2** | 判别稳 + 校准漂 | `Fig2_判别稳与校准漂` | 正文 |
> | **Fig. 3** | 三评分校准漂移对比 | `Fig3_三评分校准漂移对比` | 正文 |
> | **Fig. 4** | 规模分层 + 临床影响 | `Fig4_规模分层与临床影响` | 正文 |
> | **Fig. 5** | 重校准与收缩收益（原学习曲线/分层收缩/MIMIC 迁移三图合并为 a–d 四面板） | `Fig5_重校准与收缩收益` | 正文 |
> | **Supplementary Fig. S1** | 病例组合阶梯 | `SuppFigS1_病例组合阶梯` | 补充 |
> | **Supplementary Fig. S2** | MIMIC 在多中心分布中的位置 | `SuppFigS2_MIMIC在多中心分布中的位置` | 补充 |
> | **Supplementary Fig. S3** | 同一中心两年校准偏移的稳定性 | `SuppFigS3_同一中心两年校准偏移的稳定性` | 补充 |
> | **Table 1** | 三评分漂移汇总 | 正文内（可编辑格式，≤1 页） | 正文 |
> | **Supplementary Table S1** | 队列特征 | 补充 | 补充 |
> | **Supplementary Table S2** | τ² 四框架 | 补充 | 补充 |
> | **Supplementary Note S1** | 预注册分析计划与披露 | 补充 | 补充 |
>
> **统计报告规则（Sci Rep 硬性）**：Results 中每一处 P 值都写明检验名称、进入该检验的观察数、
> 单/双尾、α 水平与比较对象。**分析 A–H 不含假设检验**，其数值为估计值，区间为 P10–P90
> 百分位而非置信区间——**正文须明写这一点**。

---

## Results

### Cohort and study setting

The eICU-CRD cohort comprised 30,796 patients from 187 hospitals, of whom 3,901 (12.7%) died in
hospital; 103 hospitals met the pre-specified centre-level eligibility criterion of ≥ 100 patients and
≥ 10 in-hospital deaths and entered the centre-level analyses (Fig. 1). The MIMIC-IV cohort comprised
8,579 patients from one academic centre, of whom 1,654 (19.3%) died (Table 1;
Supplementary Table S1).

### Calibration varies widely across centres while discrimination does not

For SOFA, the pooled model discriminated moderately (AUC 0.732) and this varied little between
hospitals: the per-hospital AUC ranged from 0.649 to 0.812 (median 0.738), a spread of 0.16
(Fig. 2). Calibration, in contrast, varied substantially (Fig. 3, Table 1). Between-hospital
heterogeneity in the calibration-in-the-large offset was high (**I² = 75.4%**, between-centre variance
τ² = 0.131), and the observed-to-expected (O/E) mortality ratio ranged from **0.69 to 1.54** across
hospitals (10th to 90th percentile; median 0.96); a 2.2-fold spread (Fig. 3).

The pattern was not specific to SOFA. OASIS (pooled AUC 0.728; **I² = 79.8%**; O/E 0.71–1.57) and
SAPS-II (pooled AUC 0.761; **I² = 70.4%**; O/E 0.69–1.49) showed heterogeneity of comparable
magnitude (Table 1, Fig. 3). Because all three scores are established, widely used instruments fitted
with the same pipeline, this consistency indicates that between-centre calibration drift is a
property of the setting rather than of any single instrument.

Drift was not confined to a systematic offset. The per-hospital calibration slope (intercept free)
ranged from 0.720 to 1.639 (10th–90th percentile; median 1.088): the
**risk gradient itself** differs between hospitals, not merely the baseline event rate.

For the descriptive analyses in this section and the four that follow, the reported quantities are
estimates, not tests: **no hypothesis test was performed on the between-centre variation, the
differences between scores, or the case-mix comparisons**; ranges are 10th and 90th percentiles
across hospitals, not confidence intervals.

### Measured case-mix does not explain the drift

We next asked whether the measured case-mix of each hospital explains its offset. We fitted a ladder of
nested models (M1: the score alone; M2: the score with age and sex; M3: the score with age,
sex, comorbidity burden and invasive ventilation) and recomputed the between-centre heterogeneity at
each step (Supplementary Fig. S1). Adding age and sex raised the pooled AUC by only 0.009 (0.732 to
0.741) and left I² essentially unchanged (75.4% to 75.2%). Adding comorbidity burden and invasive
ventilation raised the AUC by a further 0.011 (to 0.752) and lowered I² to 70.1%, a reduction of
5.2 percentage points; τ² fell from 0.131 to 0.106.

Because M3 also carries a smaller analysis set (27,236 patients, 97 hospitals, against 30,796 and 103 for M1 and M2), refitting the M1 model on exactly those patients and hospitals gave I² = 73.49%: of the 5.2-percentage-point fall from M1 to M3, 1.9 points are attributable to the analysis set and 3.4 to the covariates (Supplementary Fig. S1).

Measured case-mix therefore accounts for only a small share of the between-centre variation: four
clinically relevant covariates, added together, explain around 5 percentage points of I² against a
baseline of 75%. **The remaining variation is reported here as residual between-hospital variation. It
is not attributed to any particular cause**; unmeasured differences in case-mix (disease spectrum,
referral patterns, pre-ICU course) and in care organisation would each produce the same pattern, and
this study is not designed to distinguish them.

### A single-centre model sits mid-distribution among centres

Applying the eICU-fitted SOFA model to MIMIC-IV, discrimination was preserved (AUC 0.722 versus 0.732
within eICU), but calibration shifted: observed mortality was 19.3% against a model prediction of
16.5%, giving an O/E ratio of 1.17 and a calibration offset of *a* = +0.221 (Supplementary Fig. S2).
MIMIC-IV's higher recorded Charlson index (3.5 vs 0.9) reflects more complete ICD coding, not
case-mix difference; the model has no comorbidity term.

That offset placed MIMIC-IV at the **66th percentile** of the 103 eICU hospitals: a single-centre
development cohort is no outlier here, it sits inside the multicentre distribution — consistent with
the general observation that a model developed in one centre systematically mis-estimates risk in
another, without any centre being unusual.

### Drift strengthens rather than shrinks with centre size

If apparent between-centre variation were driven by sampling noise, the smallest hospitals (whose
offsets are least precisely estimated) should show the highest apparent heterogeneity. The opposite
was observed (Fig. 4a). Stratifying the 103 centres into tertiles by sample size, I² rose
from 56.7% in the smallest tertile (36 centres; median 145 patients) to 69.8% in the middle tertile
(33 centres; median 225 patients) and 83.9% in the largest (34 centres; median 386 patients). The
absolute between-centre variance followed the same pattern, rising from τ² = 0.093 to 0.117 to 0.143.

The variation is therefore a genuine between-hospital difference rather than an artefact of imprecise
estimation in small samples. The 84 hospitals below the centre-level threshold are smaller and less
severely ill (median 47 patients, 9.0% mortality versus 224 and 12.7%; Supplementary Table S4).

### Calibration offset is not a stable attribute of a hospital

eICU-CRD covers only the calendar years 2014 and 2015, so year-to-year stability was assessed by
splitting each hospital's patients by year. Of the 103 eligible centres, **88 contributed ≥ 50 patients
and ≥ 5 in-hospital deaths in each year** (Supplementary Fig. S3).

The two years' offsets correlated only moderately (Pearson *r* = +0.586; P = 2.0 × 10⁻⁹, two-sided
test of *r* = 0 across 88 hospitals; Spearman ρ = +0.563), so that a hospital's offset in 2014 explained
about a third of the variance in its 2015 offset. The median absolute difference between the two years
was 0.331 (10th–90th percentile 0.12–0.83). Decomposing the variance, the within-hospital (temporal)
component was 0.102 against a total between-hospital variance of 0.246, so that **41.6% of the apparent
between-centre variance was a within-centre, year-to-year component**. There was also a systematic
downward shift between the two years (mean −0.149; *t* = −3.09 across 88 hospitals, P = 0.002,
two-sided).

**Because only two consecutive years are available, this analysis addresses year-to-year stability and
does not support any statement about a long-term temporal trend.**

### Drift changes what a risk threshold means at the bedside

We next quantified the drift's consequence for
threshold-based decisions. For each
hospital and each of four decision thresholds, we computed net benefit and the observed mortality among
patients whose predicted risk exceeded the threshold (Fig. 4b; Supplementary Table S1).

At a decision threshold of 0.20, the median proportion of patients flagged as high-risk was 12.8%, and
the **observed mortality among those patients ranged from 15% to 52%** (10th to 90th percentile;
median 33.3%); a 3.5-fold spread for the same model and the same threshold. Net benefit was positive
in the median hospital (+0.021) but was **negative in 17.0% of centres** (positive in the remainder),
meaning acting on the
model would have been worse than treating everyone as high-risk. Negative net benefit rose from 6.2% at threshold 0.10 to 21.4% at 0.30 and 22.3% at 0.40.

### Naive local recalibration carries a small-sample penalty

The findings above raise the obvious question: why not recalibrate the score using local data? We
examined this directly, drawing *m* patients from each hospital for local recalibration and using the
remainder for evaluation, with 100 resampling attempts per (hospital, *m*) cell, for centres with at
least 200 patients and at least 2*m* in all (*m* ∈ {0, 25, 50, 100, 200}; Fig. 5a).

The answer was counter-intuitive. Re-estimating the intercept on 25 local patients **made calibration
worse than not recalibrating at all**: the proportion of resampling attempts landing within ±10% of
perfect O/E fell from 21.4% (no recalibration) to 15.3%, and the median residual |*a*| rose from 0.308
to 0.448 (Fig. 5b). Naive recalibration injects estimation noise that outweighs the signal at small
sample sizes. Success improved gradually with *m* (20.0% at 50 patients, 25.5% at 100, and 34.3%
at 200), but **the pre-specified criterion of a 50% success rate was never reached within 200 local
patients**, which is reported here as a negative finding. Under the prespecified ±20% band the same
strategies rose steeply (S1: 30.6% at 25 and 62.8% at 200) while the penalty
against no recalibration (41.7%) persisted at 25 (Supplementary Table S5).

Estimating a second parameter did not help. Re-estimating both intercept and calibration slope was
worse than intercept-only at every sample size; at *m* = 25 the success rate was 13.7% and the median
residual |*a*| was 0.545, against 15.3% and 0.448 for the intercept-only strategy.

The number of hospitals contributing to each cell is reported throughout, because the requirement
*n* ≥ 2*m* progressively removes smaller centres: 103 centres at *m* ≤ 50, 59 at *m* = 100, and 13 at
*m* = 200.

### Empirical-Bayes shrinkage removes the small-sample penalty

We then tested whether shrinking each offset toward the pooled mean recovers small-sample performance
(Fig. 5c). Four strategies were compared on identical draws: no
recalibration (S0), naive intercept-only (S1), naive intercept plus slope (S2), and empirical-Bayes
shrinkage of the intercept (S3), with the shrinkage target and between-centre variance estimated by
leave-one-centre-out cross-fitting. The shrinkage weight *λ* is a reliability weight: when *SE*²
dominates *τ*², λ→0 and the local estimate collapses to the pooled mean; when *τ*² dominates, λ→1
and it is retained.

At 25 local patients, shrinkage achieved a ±10% success rate of **24.3%** against 15.5% (naive
recalibration) and 21.4% (no recalibration), outperforming both at the sample
size at which naive recalibration is harmful (Fig. 5c). Paired on identical draws, the difference
between S3 and S1 at *m* = 25 was **+9.05 percentage points** (19,678 paired (hospital, replicate)
observations; two-sided Wilcoxon signed-rank test, P = 3.7 × 10⁻¹¹²). At *m* = 100 the paired difference
was +4.65 percentage points. The shrinkage weight adapted to local sample size as expected, with median
λ of 0.234, 0.374, 0.536 and 0.712 at *m* = 25, 50, 100 and 200 respectively; the strategy shrinks
hardest precisely where the local estimate is least reliable.

**The pre-specified criterion for this analysis was met** (at *m* = 25, S3 exceeded S1; at *m* ≥ 100, S3
was not worse than S1 by more than 5 percentage points).

The learning-curve and shrinkage analyses use independent resampling schemes (100 attempts per cell
vs 200 paired draws); comparisons are made within, not between, panels.

### Shrinkage parameters transfer across databases

To test whether the shrinkage parameters generalise beyond the database in which they were estimated, we
treated MIMIC-IV as a single new centre and fixed the shrinkage target (ā = +0.030) and between-centre
variance (τ² = 0.131) at their eICU values, never re-estimating them on MIMIC-IV (Fig. 5d). The true
offset to recover was *â* = +0.221.

At 25 local patients drawn from MIMIC-IV, naive recalibration achieved a ±10% success rate of 23.5%,
whereas shrinkage achieved **47.0%**; a paired difference of **+23.5 percentage points** (two-sided
Wilcoxon signed-rank test across 200 paired resampling attempts, P = 6.3 × 10⁻⁷). Shrinkage outperformed
naive recalibration at every sample size: +19.0 points at 50 patients (P = 4.1 × 10⁻⁶), +15.5 at 100
(P = 3.8 × 10⁻⁶), +13.0 at 200 (P = 6.0 × 10⁻⁵), and +4.0 at 400 (P = 0.059, not significant at
α = 0.05, two-sided).

Expressed in terms of local data requirement, **25 local patients combined with shrinkage reached the
success rate that naive recalibration attained only with roughly 150 local patients** (naive: 40.5% at
100 and 53.0% at 200; interpolation ≈ 152); an approximately six-fold reduction. That comparison crosses resampling schemes (Fig. 5c vs 5d) and is illustrative. The advantage narrows as the local sample
grows, since naive estimators become adequate with more data.

**The pre-specified criterion for this analysis was met** (at *m* = 25, S3 exceeded both S1 and S0).

**This analysis tests whether the shrinkage parameters transfer across databases. It is not multicentre
external validation of the strategy**, which can only be evaluated within eICU itself, as reported
above. The two are reported separately and are not conflated.

### The between-centre variance depends on the estimation framework

The between-centre variance τ² underlying every result above was estimated by DerSimonian–Laird. As a
pre-specified analysis we re-estimated it under three further frameworks: Paule–Mandel, restricted
maximum likelihood (REML), and a one-stage random-intercept multilevel logistic model fitted to
patient-level data (Supplementary Table S2).

The three two-stage estimators agreed closely: τ² = 0.1312 (DerSimonian–Laird), 0.1261 (Paule–Mandel)
and 0.1299 (REML), a relative range of 3.9%, within the pre-specified 25% bound. **The one-stage
multilevel estimate did not agree**: fitted to 26,436 patients across 103 centres, it gave τ² = 0.0648,
**50.1% below the median of the two-stage estimates**, exceeding the pre-specified 50% bound. An
independent marginal-likelihood calculation (τ² = 0.0706) corroborated the multilevel value. **This
second clause of the pre-specified criterion was therefore not met, and is reported as a negative
finding.**

A plausible mechanism is that the two-stage calibration offsets are computed with the calibration slope
fixed at 1, whereas the observed per-hospital slopes range from 0.720 to 1.639 (10th to 90th
percentile). Variation in slope would be absorbed into the intercept under a fixed-slope model,
inflating the apparent between-centre intercept variance. This mechanism is offered as an explanation of
the disagreement, not as an established finding.

**The principal conclusions do not depend on which estimate is used.** I² is computed from Q and the
standard errors and is independent of τ², so the heterogeneity of 75.4% is unaffected, as are the
direction and magnitude of the discrimination–calibration dissociation. To test the empirical-Bayes
result directly, we re-ran it holding τ² fixed at each of three candidate values (0.1312,
DerSimonian–Laird; 0.0706, marginal likelihood; 0.0648, multilevel) on the same
resampling draws used above, giving three parallel sensitivity tables (Supplementary Table S3). At
*m* = 25 the shrinkage strategy outperformed naive recalibration under all three values of τ² (+9.1,
+6.7 and +6.5 percentage points respectively; all *P* < 10⁻⁵⁹), so the pre-specified criterion was met.

Two consequences follow, and both are reported. **First, the size of the advantage depends on τ²**: at
25 local patients it fell from +9.1 to +6.7
to +6.5 percentage points as τ² decreased, because a smaller τ² implies
heavier shrinkage toward the pooled mean, which pulls remote centres back further than the data warrant.
**Second, the advantage shrinks as the local sample grows, and at 200 patients it is no longer
statistically detectable for the two smaller values of τ²**
(+0.2 percentage points, P = 0.83, and
+0.2, P = 0.89; two-sided Wilcoxon
signed-rank test, α = 0.05), while remaining at +2.0 percentage points
(P = 0.035) under DerSimonian–Laird. Shrinkage is therefore a strategy for
small local samples, not a general replacement for naive estimation.

*Note on the comparison above.* The primary analysis estimated τ² separately within each
leave-one-centre-out fold, whereas the table above holds τ² fixed at each candidate point value; the two
analyses therefore differ slightly (by 0.1–0.2 percentage points at *m* ≥ 50, and not at all at
*m* = 25), which reflects that design difference. The naive column agrees exactly with the primary
analysis at every sample size, confirming that the resampling draws and the naive estimates are
identical across the two.

*Note on the multilevel value.* The multilevel τ² used here is 0.0648, the square of the maximum *a
posteriori* standard deviation (0.2545) reported in Supplementary Table S2; the two are one and the same
value. Maximum *a posteriori* estimation of a variance component is sensitive to initialisation, and
repeated fits give standard deviations in the range 0.247–0.255 (τ² 0.061–0.065). A sensitivity run at
τ² = 0.0610 gave a success rate of 21.6% rather than 21.7% at 25 local patients, an immaterial
difference; that run is retained in the repository so the difference can be inspected.
