# Title Page

Discrimination transports, calibration does not: calibration drift in severity scoring
across 187 intensive-care units

⟨First Author Full Name⟩¹, ⟨Second Author Full Name⟩¹, Tiantian Zhang²*

¹ Zhejiang Chinese Medical University, Hangzhou, Zhejiang, China

² Xianju People's Hospital, Zhejiang Southeast Campus of Zhejiang Provincial People's Hospital,
Affiliated Xianju's Hospital, Hangzhou Medical College, Xianju, Taizhou, Zhejiang, China

Corresponding author: Tiantian Zhang, Xianju People's Hospital, Xianju, Taizhou, Zhejiang, China.
Email: ⟨EMAIL⟩

---

# Abstract

Severity scores are often assumed to transport between hospitals. In a secondary analysis of eICU-CRD (30,796 patients aged ≥65 years from 187
hospitals) we examined whether such scores discriminate and calibrate alike across centres. Discrimination was moderate and nearly constant (pooled AUC 0.732 for SOFA;
per-centre AUC 0.649–0.812), whereas calibration varied substantially: between-centre I² was
75.4% and the observed-to-expected mortality ratio ranged from 0.69 to 1.54, a 2.2-fold spread.
Calibration slopes ranged from 0.72 to 1.64, indicating drift in the risk gradient. Drift
persisted after adjustment for measured case-mix, strengthened with centre size, and was
temporally unstable (split-half r = 0.586). At a decision threshold of 0.20,
mortality among patients flagged high-risk ranged from 15% to 52%, and net benefit was negative
in 17–22% of centres. Naive local recalibration proved harmful at small sample sizes: with 25
local patients it performed worse than no recalibration (success rate 15.5% versus 21.4%), and
even at 200 patients only 34.3% of resamples met the pre-specified ±10% criterion, a threshold
never reached. Empirical-Bayes shrinkage of the local calibration offset reversed this,
outperforming naive recalibration at 25 patients (24.3% versus 15.5%; two-sided P = 3.7 × 10⁻¹¹²)
and transferring to MIMIC-IV without refitting. Discrimination transports; calibration
does not.

**Keywords.** Intensive care · Calibration · Severity score · External validation · Data drift · Empirical Bayes

---

## Introduction

Acute severity scores such as the Sequential Organ Failure Assessment (SOFA) [1], the Oxford Acute
Severity of Illness Score (OASIS) [2] and the Simplified Acute Physiology Score II (SAPS-II) [3] are used
across intensive care units (ICUs) to quantify illness severity, to benchmark units against one
another, and increasingly to inform decisions about the level of care a patient should receive.
Their use rests on an assumption that is rarely examined: that a given score means the same thing
about the probability of death in one hospital as it does in another.

Discrimination is the property that is usually reported. A score that ranks sicker patients above
healthier ones will retain most of that ability when it is carried from one population to another,
and a pooled area under the receiver operating characteristic curve (AUC) is a standard feature of
validation studies. Calibration — whether the predicted probability of death matches the observed
probability — is the property that determines what a risk estimate actually means at the bedside,
and it has long been recognised as the more fragile of the two [4]. Poorly calibrated algorithms can be
misleading and harmful in clinical decision-making, and calibration has been described as the
Achilles heel of predictive analytics [5]. Even so, calibration is assessed less consistently than
discrimination in published validation studies [6], and where it is assessed the finding is
typically that it does not transport.

Most published work on calibration failure addresses one of two settings. The first is temporal:
within a single environment, calibration deteriorates as clinical practice, data capture and
patient mix change, and a substantial methodological literature now exists on detecting such drift
[7] and on updating models once it has been detected [8,9]. The second is a single transfer: a model
developed in one centre is applied to one other centre or population, where miscalibration is
observed and locally corrected [10]. What has received much less attention is the *spatial*
dimension — how far calibration differs **simultaneously across many centres** in a health system
that routinely uses the same score, and how large that between-centre component is relative to the
others. This matters because the practical response to inter-centre variation is assumed to be
local recalibration, and because benchmarking systems that compare hospitals depend on the premise
that the underlying risk adjustment is comparable across them [11].

Two questions follow that have not, to our knowledge, been answered together. First, quantitatively:
when a severity score is used in 100 or more hospitals at once, how much of the variation in
observed-to-expected mortality is real between-centre variation, how much is explained by measured
case-mix, and how much is the fluctuation one would expect from sampling alone? Second, operationally:
if a hospital does decide to recalibrate locally, how many of its own patients does it need before
the recalibration improves rather than degrades its predictions?

We addressed both questions using the eICU Collaborative Research Database (eICU-CRD), a
multicentre database covering 187 hospitals, together with MIMIC-IV as a second, single-centre
database for testing whether parameters estimated in one database can be used in another. We
quantified between-centre variation in calibration for three established severity scores, tested how
much of it measured case-mix could explain, decomposed it into components attributable to centre
size and to calendar year, translated it into consequences at four decision thresholds, and
evaluated local recalibration as a function of the number of locally available patients — together
with an empirical-Bayes shrinkage alternative.

---

## Results

### Cohort and study setting

The eICU-CRD cohort comprised 30,796 patients from 187 hospitals, of whom 3,901 (12.7%) died in
hospital; 103 hospitals met the pre-specified centre-level eligibility criterion of ≥ 100 patients and
≥ 10 in-hospital deaths and entered the centre-level analyses (Fig. 1). The MIMIC-IV cohort comprised
8,579 patients from a single academic medical centre, of whom 1,654 (19.3%) died (Table 1;
Supplementary Table S1).

### Calibration varies widely across centres while discrimination does not

For SOFA, the pooled model discriminated moderately (AUC 0.732) and this varied little between
hospitals: the per-hospital AUC ranged from 0.649 to 0.812 (median 0.738), a spread of 0.16
(Fig. 2). Calibration, in contrast, varied substantially (Fig. 3, Table 1). Between-hospital
heterogeneity in the calibration-in-the-large offset was high (**I² = 75.4%**, between-centre variance
τ² = 0.131), and the observed-to-expected (O/E) mortality ratio ranged from **0.69 to 1.54** across
hospitals (10th to 90th percentile; median 0.96) — a 2.2-fold spread (Fig. 3).

The pattern was not specific to SOFA. OASIS (pooled AUC 0.728; **I² = 79.8%**; O/E 0.71–1.57) and
SAPS-II (pooled AUC 0.761; **I² = 70.4%**; O/E 0.69–1.49) showed heterogeneity of comparable
magnitude (Table 1, Fig. 3). Because all three scores are established, widely used instruments fitted
with the same pipeline, this consistency indicates that between-centre calibration drift is a
property of the setting rather than of any single instrument.

Drift was not confined to a systematic offset. The per-hospital calibration slope, estimated with the
intercept free, ranged from 0.720 to 1.639 (10th to 90th percentile; median 1.088), indicating that the
**risk gradient itself** differs between hospitals and not merely the baseline event rate.

For the descriptive analyses in this section and the four that follow, the reported quantities are
estimates rather than tests. No hypothesis test was performed on the between-centre variation, the
differences between scores, or the case-mix comparisons; ranges given are 10th and 90th percentiles
across hospitals, not confidence intervals.

### Measured case-mix does not explain the drift

We next asked whether the measured case-mix of each hospital explains its offset. We fitted a ladder of
nested models — the score alone (M1), the score with age and sex (M2), and the score with age, sex,
comorbidity burden and invasive ventilation (M3) — and recomputed the between-centre heterogeneity at
each step (Supplementary Fig. S1). Adding age and sex raised the pooled AUC by only 0.009 (0.732 to
0.741) and left I² essentially unchanged (75.4% to 75.2%). Adding comorbidity burden and invasive
ventilation raised the AUC by a further 0.011 (to 0.752) and lowered I² to 70.1%, a reduction of
5.2 percentage points; τ² fell from 0.131 to 0.106.

Because M3 also carries a smaller analysis set (27,236 patients and 97 hospitals, against 30,796 and 103 for M1 and M2), we separated the two contributions directly: refitting the M1 model — the score alone — on exactly the patients and hospitals used by M3 gave I² = 73.49%. Of the 5.2-percentage-point fall from M1 to M3, 1.9 points were therefore attributable to the change in analysis set and 3.4 points to the addition of the covariates themselves. The reduction reflects the covariates; the change in analysis set is the smaller contributor (Supplementary Fig. S1).

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

That offset placed MIMIC-IV at the **66th percentile** of the distribution of the 103 eICU hospitals. A
single-centre development cohort is therefore not an outlier in this setting — it sits well inside the
multicentre distribution. This is consistent with the general observation that a model developed in one
centre will systematically mis-estimate risk in another, without any centre being unusual; the variation
being sampled is a property of the set of centres.

### Drift strengthens rather than shrinks with centre size

If apparent between-centre variation were driven by sampling noise, the smallest hospitals — whose
offsets are least precisely estimated — should show the highest apparent heterogeneity. The opposite
was observed (Fig. 4a). Stratifying the 103 centres into tertiles by sample size, I² rose
from 56.7% in the smallest tertile (36 centres; median 145 patients) to 69.8% in the middle tertile
(33 centres; median 225 patients) and 83.9% in the largest (34 centres; median 386 patients). The
absolute between-centre variance followed the same pattern, rising from τ² = 0.093 to 0.117 to 0.143.

The variation is therefore a genuine between-hospital difference rather than an artefact of imprecise
estimation in small samples.

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

We next quantified the consequence of the observed drift for threshold-based decisions. For each
hospital and each of four decision thresholds, we computed net benefit and the observed mortality among
patients whose predicted risk exceeded the threshold (Fig. 4b; Supplementary Table S1).

At a decision threshold of 0.20, the median proportion of patients flagged as high-risk was 12.8%, and
the **observed mortality among those patients ranged from 15% to 52%** (10th to 90th percentile;
median 33.3%) — a 3.5-fold spread for the same model and the same threshold. Net benefit was positive
in the median hospital (+0.021) but was **negative in 17.0% of centres**, meaning that acting on the
model would have been worse than treating everyone as high-risk in those hospitals. The proportion of
centres with negative net benefit rose from 6.2% at threshold 0.10 to 21.4% at 0.30 and 22.3% at 0.40.

### Naive local recalibration carries a small-sample penalty

The findings above raise the obvious question: why not recalibrate the score using local data? We
examined this directly, drawing *m* patients from each hospital for local recalibration and using the
remainder for evaluation, with 100 resampling attempts per (hospital, *m*) cell, for centres with at
least 200 patients and at least 2*m* in all (*m* ∈ {0, 25, 50, 100, 200}; Fig. 5a).

The answer was counter-intuitive. Re-estimating the intercept on 25 local patients **made calibration
worse than not recalibrating at all**: the proportion of resampling attempts landing within ±10% of
perfect O/E fell from 21.4% (no recalibration) to 15.3%, and the median residual |*a*| rose from 0.308
to 0.448 (Fig. 5b). Naive recalibration injects estimation noise that outweighs the signal at small
sample sizes. Performance improved gradually with *m* — 20.0% at 50 patients, 25.5% at 100, and 34.3%
at 200 — but **the pre-specified criterion of a 50% success rate was never reached within 200 local
patients**, which is reported here as a negative finding.

Estimating a second parameter did not help. Re-estimating both intercept and calibration slope was
worse than intercept-only at every sample size; at *m* = 25 the success rate was 13.7% and the median
residual |*a*| was 0.545, against 15.3% and 0.448 for the intercept-only strategy.

The number of hospitals contributing to each cell is reported throughout, because the requirement
*n* ≥ 2*m* progressively removes smaller centres: 103 centres at *m* ≤ 50, 59 at *m* = 100, and 13 at
*m* = 200.

### Empirical-Bayes shrinkage removes the small-sample penalty

We then tested whether shrinking each hospital's estimated offset toward the pooled mean could recover
the small-sample performance (Fig. 5c). Four strategies were compared on identical draws: no
recalibration (S0), naive intercept-only (S1), naive intercept plus slope (S2), and empirical-Bayes
shrinkage of the intercept (S3), with the shrinkage target and between-centre variance estimated by
leave-one-centre-out cross-fitting.

At 25 local patients, shrinkage achieved a ±10% success rate of **24.3%** against 15.5% for naive
recalibration and 21.4% for no recalibration: the strategy outperformed both alternatives at the sample
size at which naive recalibration is harmful (Fig. 5c). Paired on identical draws, the difference
between S3 and S1 at *m* = 25 was **+9.05 percentage points** (19,678 paired (hospital, replicate)
observations; two-sided Wilcoxon signed-rank test, P = 3.7 × 10⁻¹¹²). At *m* = 100 the paired difference
was +4.65 percentage points. The shrinkage weight adapted to local sample size as expected, with median
λ of 0.234, 0.374, 0.536 and 0.712 at *m* = 25, 50, 100 and 200 respectively — the strategy shrinks
hardest precisely where the local estimate is least reliable.

**The pre-specified criterion for this analysis was met** (at *m* = 25, S3 exceeded S1; at *m* ≥ 100, S3
was not worse than S1 by more than 5 percentage points).

*Note on the two success rates for naive recalibration.* The learning-curve analysis reports 15.3% at *m* = 25, whereas the shrinkage analyses report 15.5%. Both are correct: the first uses 100 resampling attempts per cell and the second 200 with a paired design, so they are independent draws. Comparisons are made within, not between, panels.

### Shrinkage parameters transfer across databases

To test whether the shrinkage parameters generalise beyond the database in which they were estimated, we
treated MIMIC-IV as a single new centre and fixed the shrinkage target (ā = +0.030) and between-centre
variance (τ² = 0.131) at their eICU values, never re-estimating them on MIMIC-IV (Fig. 5d). The true
offset to recover was *â* = +0.221.

At 25 local patients drawn from MIMIC-IV, naive recalibration achieved a ±10% success rate of 23.5%,
whereas shrinkage achieved **47.0%** — a paired difference of **+23.5 percentage points** (two-sided
Wilcoxon signed-rank test across 200 paired resampling attempts, P = 6.3 × 10⁻⁷). Shrinkage outperformed
naive recalibration at every sample size: +19.0 points at 50 patients (P = 4.1 × 10⁻⁶), +15.5 at 100
(P = 3.8 × 10⁻⁶), +13.0 at 200 (P = 6.0 × 10⁻⁵), and +4.0 at 400 (P = 0.059, not significant at
α = 0.05, two-sided).

Expressed in terms of local data requirement, **25 local patients combined with shrinkage reached the
success rate that naive recalibration attained only with roughly 150 local patients** (naive
recalibration reached 40.5% at 100 patients and 53.0% at 200; linear interpolation gives approximately
152) — an approximately six-fold reduction. As expected, the advantage narrowed as the local sample
grew, since naive estimators become adequate once enough data are available.

**The pre-specified criterion for this analysis was met** (at *m* = 25, S3 exceeded both S1 and S0).

**This analysis tests whether the shrinkage parameters transfer across databases. It is not multicentre
external validation of the strategy**, which can only be evaluated within eICU itself, as reported
above. The two are reported separately and are not conflated.

### The between-centre variance depends on the estimation framework

The between-centre variance τ² underlying every result above was estimated by DerSimonian–Laird. As a
pre-specified analysis we re-estimated it under three further frameworks: Paule–Mandel, restricted
maximum likelihood (REML), and a one-stage random-intercept multilevel logistic model fitted to
patient-level data (Supplementary Table S2).

The three two-stage estimators agreed closely — τ² = 0.1312 (DerSimonian–Laird), 0.1261 (Paule–Mandel)
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
result directly, we re-ran it holding τ² fixed at each of three candidate values — 0.1312
(DerSimonian–Laird), 0.0706 (marginal likelihood) and 0.0648 (multilevel) — on the same
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

---

## Discussion

In 103 hospitals using the same scores and the same pipeline, a SOFA-based model discriminated
consistently (per-centre AUC 0.649–0.812) while its calibration varied by more than twofold
(observed-to-expected mortality 0.69–1.54; between-centre I² = 75.4%). Measured case-mix explained
little of that variation, the variation grew rather than shrank in the largest and therefore most
precisely estimated centres, a hospital's offset in one year explained only about a third of its
offset in the next, and at a decision threshold of 0.20 the observed mortality among patients
flagged high-risk ranged from 15% to 52% across centres, with net benefit negative in 17.0% of them.
The response that follows most naturally from these findings — recalibrate locally — turned out to
carry a penalty: recalibrating on 25 local patients was worse than not recalibrating at all.
Shrinking the local estimate toward the pooled mean removed that penalty, and the parameters needed
to do so could be estimated once and used in a second database without refitting.

**Relation to prior work on calibration drift.** The closest antecedents to the present study
treat calibration drift as a *temporal* phenomenon within one environment: Han et al. detected
increasing miscalibration over time using online stochastic gradient descent and adaptive windows
[7], and Zhang et al. proposed lifelong machine learning to counter it across four tumour datasets
[12]. Both are well-suited to their question and neither is contradicted here. The present study
addresses the orthogonal question — the *spatial* component — and does so at a scale rarely
attempted: rather than one environment followed over time or one transfer from centre to centre
[10,13], we observed 103 centres simultaneously and were able to partition the resulting variance. A
clinically important corollary is that the two sources are not interchangeable. A hospital offset
that is 41.6% temporal in origin cannot be fixed by a permanent recalibration, however large the
sample used to fit it, and a hospital-to-hospital difference that persists after case-mix adjustment
cannot be explained by improvement over time. Decomposing them would require a database spanning
several years, which eICU-CRD does not.

**Relation to the model-updating literature.** A mature methodological literature describes how to
evaluate and update a prediction model, including when recalibration is appropriate [8,9,14,15], and
empirical comparisons of update strategies exist [16,17]. Those recommendations are generally
presented as unqualified: if calibration in the target setting is poor, recalibrate. Our findings
qualify rather than contradict them. The literature assumes a local sample large enough for the recalibration to be estimated
reliably. Formal minimum sample sizes exist for external validation [18], but they address the
precision of the calibration estimate rather than whether recalibration improves decisions. We
found that with 25 local patients naive recalibration lowered the proportion of resamples reaching
±10% accuracy from 21.4% to 15.3%, that estimating a second parameter (the calibration slope) made it
worse still, and that a 50% success rate was not reached even at 200 patients. That missing quantity — how many local patients are needed before recalibration helps rather
than harms — appears to govern whether the recommendation helps.

**The shrinkage result and its limits.** Empirical-Bayes shrinkage of the local offset toward the
pooled mean recovered small-sample performance (24.3% versus 15.5% at 25 patients) and transferred to
MIMIC-IV with parameters fixed from eICU. Two qualifications belong with that result. First, the
advantage is a property of small local samples: at 200 local patients it fell to between +0.2 and
+2.0 percentage points depending on the estimator of the between-centre variance, and was no longer
statistically detectable for the smaller of those. Second, its magnitude depends on τ², the
between-centre variance, which itself was not agreed across estimation frameworks: our pre-specified
criterion for agreement was only partly met, with the one-stage multilevel estimate falling 50.1%
below the two-stage values. A plausible explanation is that two-stage calibration offsets are
computed with the slope fixed at 1 while observed slopes ranged from 0.720 to 1.639, so that slope
variation is absorbed into the intercept; we present this as a possible mechanism rather than a
finding.

**Consequences for benchmarking.** Benchmarking systems for ICU care are expanding internationally
[19,20], and such systems presume that observed-to-expected ratios are comparable between
institutions. Our results indicate that this premise requires active verification: an observed-to-
expected ratio of 0.69 in one hospital and 1.54 in another, under the same model, is not a
difference in performance that a benchmark can safely interpret. Because the variation is only
partly temporal and not explained by measured case-mix, neither a stable unit-level adjustment nor a
one-off recalibration resolves it. The emerging focus on post-deployment monitoring and lifecycle
governance of clinical models [21] would be strengthened by treating centre-specific calibration as
a quantity to be monitored rather than assumed.

**Why STROBE rather than TRIPOD.** The data are clustered by hospital, which is the structure the
TRIPOD-Cluster statement was written to address [22], and reporting standards for prediction models
have continued to develop with TRIPOD+AI [23]. We report using STROBE [24] with the RECORD extension for routinely collected health
data [25], because no prediction model
was developed or deployed for clinical use in this study: the pooled model served as a measurement
instrument for quantifying drift, and the object of the study is the between-centre variation
itself, not the performance of a model intended for patient-level decisions. We have nonetheless
reported the elements that matter for clustered data — the clustering level, the number of centres
per estimate, and the resampling design.

**Limitations.** First, both databases were collected for purposes other than this study, as is inherent in the
secondary-use design. Two consequences follow, and both are limitations of that design rather than of the analysis. Misclassification in the underlying records — in the severity scores, in comorbidity coding and in the recorded discharge status — cannot be detected here, and its
direction and magnitude could not be quantified. And because eICU-CRD covers only 2014 and
2015, we could not assess how eligibility for the cohort, or the coding practices behind it,
changed over time. The year-to-year analysis reported here addresses stability across two
consecutive years and nothing more, and the study therefore quantifies the spatial component of
drift while providing no evidence about longer-term temporal trends. Second, MIMIC-IV is a single centre, so the external analysis tests whether the shrinkage
parameters transfer across databases; it is not multicentre external validation of the strategy,
which can only be evaluated within eICU itself. Third, the variation not explained by measured
case-mix is described here as residual between-hospital variation. Unmeasured differences in
disease spectrum, referral patterns and pre-ICU course would produce the same pattern, and this
study is not designed to attribute the variation to any of them — no conclusion about quality of
care is drawn. Fourth, the two databases record comorbidity differently. The mean Charlson index in
MIMIC-IV (3.5) is far higher than in eICU-CRD (0.9), reflecting more complete inpatient ICD coding
in MIMIC-IV rather than a difference in case-mix. Because the external analysis uses a single-score
SOFA model that contains no comorbidity term, this does not affect any result reported here, but it
limits how far the two cohorts can be compared on measured case-mix. Fifth, we studied three
established scores and one pooled model specification; other specifications, and scores not
evaluated here, may behave differently. Sixth, the empirical-Bayes parameters were estimated in a
single database, and although they transferred to a second, the extent to which they generalise to
other health systems and other score families remains open.

**Conclusion.** Discrimination transports; calibration does not, and the difference is large enough
to change what a risk threshold means in different hospitals. Local recalibration is not the
remedy it is usually assumed to be unless a centre has several hundred of its own patients, and
shrinking the local estimate toward the pooled mean makes it useful far sooner. What this study
offers is a statistical recalibration strategy and a measurement of how much local data it needs —
not a clinical recommendation.

---

## Study design and setting

We performed a retrospective secondary analysis of two publicly available, de-identified, multicentre
critical-care databases: the eICU Collaborative Research Database (eICU-CRD v2.0) and MIMIC-IV v3.1.
Neither database was collected for the purpose of this study, and no new data were generated. The study
is reported in accordance with the STROBE statement. The study protocol was not registered; the analysis
plans written before each analysis was executed are reproduced verbatim as Supplementary Item S1
(together with their file timestamps, an explicit disclosure of one timestamp defect, and a classification
of analyses as descriptive or confirmatory).

The research question was whether an acute severity score means the same thing about mortality risk in
different hospitals, and, if it does not, what it takes to recalibrate it locally.

## Data sources

Both datasets are third-party, publicly available databases obtained under their respective data use
agreements through PhysioNet (https://physionet.org/).

**eICU-CRD v2.0** [26] contains data from 208 hospitals in the United States for the period 2014–2015,
comprising 200,859 intensive-care unit (ICU) stays. Access required credentialed application and
attestation of the PhysioNet data use agreement.

**MIMIC-IV v3.1** [27] contains data from Beth Israel Deaconess Medical Center, a single academic medical
centre, comprising 94,458 ICU stays. Access required completion of CITI "Data or Specimens Only"
training and a data use agreement.

No patient-level records from either database are redistributed by this study. All database access was
**read-only**; no script written for this study modified a database.

## Cohort construction

The step-wise inclusion and exclusion criteria are shown in Figure 1, and the counts reported there are
taken from the extraction stage's own count reports (`cohort/eicu_counts.json`,
`cohort/mimic_counts.json`) rather than re-derived, so that Figure 1 reflects the actual pipeline rather
than a reconstruction. Full details are given in `cohort/README.md`.

**eICU-CRD.** Of 200,859 unit stays across 208 hospitals, we retained the first ICU stay per patient
(139,367), restricted to patients aged ≥ 65 years (71,734) with an ICU length of stay ≥ 24 h
(50,138) and admitted to a medical ICU or medical–surgical ICU (31,307). We then excluded deaths within
24 h of ICU admission (n = 7), stays with an unknown hospital outcome status (n = 363), and stays in
which albumin, height and weight were all missing (n = 141). The resulting cohort comprised **30,796
patients from 187 hospitals, of whom 3,901 (12.7%) died**. The final exclusion step was carried over from
the source data-extraction protocol so that cohorts remain comparable with related work from the same
research group; this study analyses neither albumin, height nor weight, so the step affects neither the
cohort entering any analysis nor any reported result. It is reported here for transparency about the
extraction pipeline.

**MIMIC-IV.** Of 94,458 ICU stays, we retained the first ICU stay per patient (65,366), restricted to
patients aged ≥ 65 years (35,499; `anchor_age`, corrected by the difference between admission year and
anchor year), with ICU length of stay ≥ 24 h (28,607), whose first ICU stay was in a medical ICU or
medical–surgical ICU (8,629). Deaths within 24 h of ICU admission (n = 35) and stays in which albumin,
height and weight were all missing (n = 15) were excluded. The resulting cohort comprised **8,579
patients, of whom 1,654 (19.3%) died**.

**Centre-level eligibility.** For centre-level analyses a hospital had to contribute ≥ 100 patients and
≥ 10 in-hospital deaths; a hospital with no events cannot support an estimable calibration offset. This
criterion was pre-specified. **103 of 187 hospitals** met it. Hospitals below the threshold continued to
contribute to the pooled model.

## Potential sources of bias

Four sources were considered.

**Selection.** Restricting to ICU stays of at least 24 h and to medical ICUs removes short stays and
non-medical units, so the cohort does not describe all ICU admissions. Deaths within 24 h of ICU
admission were excluded because such patients cannot in principle have the severity of illness
captured by a score computed over the first ICU day; this removes 7 patients in eICU-CRD and 35 in
MIMIC-IV.

**Information.** The scores and the outcome are taken from the source databases' own records and were
not re-adjudicated. Any misclassification in the underlying records would attenuate or distort the
apparent calibration, and cannot be detected here.

**Leakage.** In the shrinkage analysis, each hospital's shrinkage parameters were estimated from the
remaining hospitals only (leave-one-centre-out cross-fitting), so no hospital's evaluation data enter
its own shrinkage parameters. In the resampling analyses the local calibration set and the evaluation
set are disjoint by construction.

**Confounding of the between-centre comparison.** No causal comparison between hospitals is made or
intended. Differences between hospitals are reported descriptively, and unmeasured differences in
disease spectrum, referral patterns and pre-ICU course could each produce the observed pattern.

## Study size and missing data

**No sample size calculation was performed.** This is a secondary analysis of two existing databases,
and the analysis used all patients meeting the eligibility criteria described above. The number of
hospitals entering the centre-level analyses was therefore a property of the data rather than of a
design decision; the pre-specified eligibility threshold (≥ 100 patients and ≥ 10 in-hospital deaths
per hospital) was fixed before any analysis was run and is reported for every cell.

**Missing data were negligible and are reported in full.** In the eICU-CRD cohort the three severity
scores, age, sex, invasive ventilation and in-hospital death were complete in every patient (0%
missing), so no imputation was performed. Charlson comorbidity index was missing in 3,560 of 30,796
patients (11.6%) in eICU-CRD (2,807 of 26,436, 10.6%, within the 103-centre analysis subset) and in
3 of 8,579 patients (0.04%) in MIMIC-IV. Comorbidity index enters only the descriptive case-mix
ladder (model M3), which therefore uses complete cases: *n* = 27,236 and 97 hospitals, against
*n* = 30,796 and 103 hospitals for M1 and M2. Because that analysis is descriptive and no
confirmatory conclusion rests on M3, we did not impute. All analyses other than the case-mix ladder
use the complete-case set defined by the cohort eligibility criteria, and that set has no missing
values on any analysis variable.

*Note on the exclusion step.* The exclusion of stays in which albumin, height and weight were all
missing (141 patients in eICU-CRD, 15 in MIMIC-IV) is a cohort-eligibility filter inherited from
the source extraction protocol; it is not a within-analysis missing-data decision, and it does not
affect any analysis variable used here.

## Severity scores

Three established severity scores were used exactly as supplied by the source extraction protocols: the Sequential
Organ Failure Assessment (SOFA) [1], the Oxford Acute Severity of Illness Score (OASIS) [2], and the Simplified
Acute Physiology Score II (SAPS-II) [3]. This study did not recompute the scores, and their derivation is
documented in the source protocols. Analysis was restricted to patients with a non-missing value for the
score being analysed; all three scores were complete in both cohorts.

**Validity of the variable definitions.** SOFA, OASIS and SAPS-II are established, previously
published and externally validated scores, used here exactly as supplied by the source extraction
protocols; their components and weights are those of the original publications and are not modified
in this study. In-hospital death is a discharge status recorded in the source databases rather than a
derived outcome, and no case-finding algorithm was applied to it. Age, sex, invasive ventilation and
Charlson comorbidity index were taken as supplied. No code list or phenotype algorithm was developed
for this study; where a variable required a derived definition, that definition is given above in full
(the calibration offset and its standard error, and the calibration slope).

## Pooled models

For each score we fitted a pooled logistic regression across the full cohort, with the score standardised
(z-score) before fitting. Models were fitted in scikit-learn (`LogisticRegression`, `C = 1.0`, i.e. L2
penalty, maximum 5,000 iterations).

**Justification of the penalised estimator.** The penalty was verified to be immaterial for this design:
refitting all seven pooled models without the penalty changed no predicted probability by more than
2.2 × 10⁻⁴ and changed no AUC by more than 1.3 × 10⁻⁶ (observed range: M1 SOFA, M1 OASIS, M1 SAPS-II,
M2, and the three M3 models; n = 30,796 for M1/M2 and n = 27,236 for M3, the latter reflecting
complete-case exclusion on comorbidity and ventilation). This is consistent with a penalty term that is
negligible relative to the log-likelihood at this sample size with one to five predictors. Both the
penalised and unpenalised refits are recoverable from the repository.

The case-mix models M2 and M3 additionally included age and sex, and comorbidity burden and invasive
ventilation respectively, entered as covariates on the same standardised scale.

## Centre-level calibration measures

Two per-hospital quantities were derived for each pooled model.

**Calibration-in-the-large offset (a_h).** For hospital *h* with fitted probabilities *p* and observed
mortality *ŷ*, we solved for *a_h* such that the mean of `expit(logit(p) + a_h)` equals *ŷ*, by bisection
over [−12, 12] to a tolerance of 10⁻⁴. *a_h* = 0 indicates that the hospital's observed mortality matches
the model's expectation; *a_h* > 0 indicates higher observed than predicted mortality. This is a
calibration-in-the-large (intercept) measure with the calibration slope fixed at 1.

The standard error of *a_h* was obtained by the delta method as
`sqrt(max(ŷ(1 − ŷ), 10⁻⁹)/n_h) / max(mean(p(1 − p)), 10⁻⁹)`, where *n_h* is the hospital's sample size.

**Calibration slope (b_h).** We additionally fitted, within each hospital, a logistic regression of the
outcome on the logit of the pooled model's predicted probability with a free intercept, and retained the
slope.

**Quantitative variables and cut-points.** All three scores, age and comorbidity burden were
analysed as continuous variables and standardised before fitting; they were not categorised. Cut-points
used in this study were fixed in advance and are not data-driven: the four decision thresholds (0.10,
0.20, 0.30, 0.40), the hospital-eligibility threshold (≥ 100 patients and ≥ 10 in-hospital deaths),
the local recalibration sample sizes (*m* ∈ {0, 25, 50, 100, 200} and, for the external analysis,
{0, 25, 50, 100, 200, 400}), the resampling attempt counts (100 for the learning-curve analysis, 200
for the shrinkage analyses), and the centre-size tertile boundaries (hospitals split by sample size
into three groups of 36, 33 and 34 hospitals, with ranges 100–181, 184–280 and 289–987 patients
respectively) were all specified in the analysis plans written before execution (Supplementary Note,
*Prespecified analysis plans*).

## Between-centre heterogeneity

For each score, per-hospital offsets were pooled by random-effects meta-analysis. Heterogeneity was summarised by *I²* [28], defined as `max(0, (Q − (k − 1))/Q) × 100`, where *Q* is the fixed-effect
Cochran statistic computed with weights 1/SE². The between-centre variance *τ²* was estimated by the DerSimonian–Laird method [29]. Because DerSimonian–Laird predates current guidance [30], *τ²* was additionally
re-estimated under three further frameworks as a pre-specified analysis (analysis K): Paule–Mandel,
restricted maximum likelihood (REML), and a one-stage random-intercept multilevel logistic model fitted
to patient-level data (`statsmodels` `BinomialBayesMixedGLM`, Laplace/maximum *a posteriori*). Analyses
A–H and J used the DerSimonian–Laird estimate; sensitivity of the principal conclusion to this choice is
reported with analysis K.

**Weighting.** Two weighting schemes appear in this work and are not interchangeable. The fixed-effect
weights (1/SE²) are used to compute *Q* and hence *τ²*, as DerSimonian–Laird specifies. The random-effects
weights (1/(SE² + *τ²*)) are used for the pooled mean and its standard error, which is the maximum
likelihood estimate under the hierarchical model `a_h ~ N(ā, τ² + SE²)`. The distinction matters for the
shrinkage analysis below and is set out in Supplementary Item S1 (§S1.6).

## Case-mix ladder

To test whether measured case-mix explains between-centre calibration drift, the same pipeline was applied
to three nested models: M1 (the score alone), M2 (score + age + sex), and M3 (score + age + sex +
comorbidity burden + invasive ventilation). Reduction in *I²* across the ladder quantifies the share of
drift attributable to the measured covariates.

## Temporal stability within hospitals

eICU-CRD covers only 2014–2015, so temporal stability was assessed as a split-half comparison of the two
calendar years. Of the 103 eligible hospitals, **88 contributed ≥ 50 patients and ≥ 5 deaths in each
year**. We report the Pearson correlation between the two years' *a_h*, the median absolute difference
\|Δ*a_h*\|, the ratio of within-hospital (temporal) variance to total between-hospital variance, and the
mean year-over-year drift. **Because only two years are available, this analysis addresses year-to-year
stability and not a long-term temporal trend.**

## Centre size and clinical impact

**Size stratification.** Hospitals were split into tertiles by sample size, and *I²* and *τ²* were
recomputed within each tertile. If apparent heterogeneity were driven by sampling noise, the stratum with
the least precise estimates (smallest hospitals) should show the *highest* apparent heterogeneity.

**Clinical impact.** For decision thresholds 0.10, 0.20, 0.30 and 0.40, each hospital's net benefit was
computed as `TP/n − (FP/n) × (p_t/(1 − p_t))` together with the observed mortality among patients
flagged above the threshold (positive predictive value).

## Local recalibration learning curve (analysis E)

For every hospital with n ≥ 200 patients, and for each *m* ∈ {0, 25, 50, 100, 200} subject to *n* ≥
2*m*, we randomly drew *m* patients as a local recalibration set and used the remaining patients as the
evaluation set; hospitals that did not satisfy *n* ≥ 2*m* at a given *m* were excluded from that cell and
*k* is reported for every cell. **Each (hospital, *m*) cell was resampled 100 times**, as pre-specified.
Two strategies were compared: re-estimating only the intercept, and re-estimating both intercept and
calibration slope.

The primary measure was the proportion of resampling attempts whose residual absolute deviation from
perfect observed-to-expected ratio was within ±10% (|O/E − 1| ≤ 0.10), **computed for each resampling
attempt and then averaged across hospitals**; a secondary measure used ±20%. Success rates are not
computed from the median residual O/E, because the resampling error is unbiased and its median therefore
converges to 1 — such a statistic measures unbiasedness rather than accuracy.

## Empirical-Bayes shrinkage (analysis I)

We evaluated four strategies on the same (hospital, *m*, replicate) draws: **S0**, no recalibration;
**S1**, naive re-estimation of the intercept only; **S2**, naive re-estimation of intercept plus
calibration slope; and **S3**, empirical-Bayes shrinkage of the intercept [31]

> *a*_EB = ā + λ · (*a*_MLE − ā), with λ = *τ²* / (*τ²* + SE²)

Both ā and *τ²* were estimated by **leave-one-centre-out cross-fitting**, so that no hospital's own
evaluation data entered its shrinkage parameters. λ decreases as SE² grows relative to *τ²*, so the
shrinkage weight adapts to local sample size — it is strongest exactly where the local estimate is least
trustworthy.

*Empirical-Bayes shrinkage target.* ā is estimated with **random-effects weights**
`Σ(a/(SE²+τ²)) / Σ(1/(SE²+τ²))`, not with the fixed-effect weights used to compute *Q* and *τ²*. The
reason is that λ above is derived from the hierarchical model `a ~ N(ā, τ² + SE²)`, under which the
maximum likelihood estimate of ā is precisely the random-effects weighted mean; using a fixed-effect
mean (the estimate implied by *τ²* = 0) while using a λ that assumes *τ²* > 0 would make the two halves
of the estimator rest on mutually contradictory assumptions. This specification was settled after the
initial analyses, is disclosed as a post-hoc correction in Supplementary Item S1 (§S1.6), and is not a
change to any pre-specified criterion. Re-running analyses A–D after the change reproduced every
pre-existing field exactly.

**Resampling.** Each (hospital, *m*) cell was resampled **200 times**, using explicitly seeded
`numpy.random.Generator` instances (`20261019 + replicate × 9973 + hospital_index × 131`).

**Comparison.** Strategies were compared by paired differences in success rate on identical draws, using
the **two-sided Wilcoxon signed-rank test** across paired (hospital, replicate) observations.

## Transfer of the shrinkage parameters to a second database (analysis J)

To test whether the shrinkage parameters generalise beyond the database in which they were estimated,
MIMIC-IV was treated as **a single new centre**, and ā and *τ²* were **fixed at their eICU values
(ā = +0.030, *τ²* = 0.131) and never re-estimated on MIMIC-IV**. The external model was the eICU-fitted
SOFA pooled model, applied using eICU's standardisation parameters. The true offset to recover, *â* =
+0.221, was computed once from the full MIMIC-IV cohort (observed 19.3% versus predicted 16.5%,
O/E = 1.17). For each *m* ∈ {25, 50, 100, 200, 400} subject to *n* ≥ 2*m*, *m* patients were drawn as
the local calibration set and the remainder served as evaluation, **200 times per cell**, with the same
seed construction as above.

**This analysis tests whether the shrinkage parameters transfer across databases. It is not
multicentre external validation of the strategy**, which can only be evaluated within eICU itself
(analysis I). The two are reported separately throughout and are not conflated.

## Analysis framework and inferential status

Analyses were assigned to one of two inferential tiers, and the assignment is reported in the manuscript
so that readers can weight the findings accordingly. **This classification was fixed after the analyses
were completed and is disclosed as such; it is not a claim that all analyses were confirmatory.**

**Descriptive / exploratory tier.** The magnitude of between-centre variation in calibration, its
comparison across three severity scores, its relation to measured case-mix, its year-to-year stability
within a given centre, its relation to centre size, and its clinical consequences at fixed decision
thresholds were estimated without pre-specified hypothesis tests. These are reported as **estimates with
interval bounds**, not as tests of a hypothesis, and no claim of statistical significance is attached to
them.

**Confirmatory tier (pre-specified criterion).** Four analyses were each planned with an explicit
criterion *and* with an explicit instruction for the case in which that criterion was not met:

- **Analysis E — local recalibration learning curve.** Criterion: report the smallest local sample
  size *m* at which the success rate reaches 50%, and state so if none is reached. **Not met** — the
  threshold was never reached within *m* = 200.
- **Analysis I — empirical-Bayes shrinkage versus naive recalibration.** Criterion: at *m* = 25 the
  shrinkage strategy must exceed naive recalibration, and at *m* ≥ 100 it must not be worse by more
  than 5 percentage points. **Met.**
- **Analysis J — transfer of the shrinkage parameters to a second database.** Criterion: at
  *m* = 25 shrinkage must exceed both naive recalibration and no recalibration. **Met.**
- **Analysis K — agreement of *τ²* across estimation frameworks.** Criterion: a relative range across
  the three two-stage estimators below 25%, and the one-stage multilevel estimate within 50% of their
  median. **Partly met** — the first clause was met (3.9%), the second was **not** (the multilevel
  *τ²* was 50.1% lower).

**Two of the four pre-specified criteria were not met, and both are reported as negative findings.** They
are not reframed after the fact: analysis E is reported as showing that naive local recalibration has a
small-sample penalty that persists to 200 patients, and analysis K is reported as a genuine disagreement
between two-stage and one-stage estimators, together with a proposed mechanism and a sensitivity analysis
demonstrating that the principal conclusion is unaffected.

**Multiplicity.** Because the confirmatory analyses were four in number and were each defined by a single
pre-specified criterion evaluated once on the full cohort, no formal adjustment for multiple comparisons was
applied. The descriptive analyses involve no hypothesis testing. Readers should interpret the interval
bounds in the descriptive tier as measures of precision, not as tests.

## Statistical reporting

Every reported *P* value is accompanied by the name of the test used to produce it, the number of
observations entering that test, whether the test was one- or two-sided, and the comparison being made.
Where two groups are compared on identical resampling draws, the comparison is paired and the two-sided
Wilcoxon signed-rank test is used; normality of the paired differences was not assumed, and a
non-parametric test was selected for that reason. The pre-specified α level was 0.05 and all reported
tests are two-sided. Group sizes are given for every analysis. Descriptive statistics are reported as the
median with the 10th and 90th percentiles for skewed quantities (because these distributions are markedly
asymmetric and small-sample), and ± indicates a standard error where stated. Analyses A–H and K contain
no hypothesis tests; the values reported for them are estimates, and the bounds reported are 10th and 90th
percentiles rather than confidence intervals. No *P* value in this manuscript is reported only as
"significant"; each is given as a number.

## Uncertainty in pooled performance estimates

Confidence intervals for the pooled AUC of each score were obtained by **cluster bootstrap**,
resampling hospitals with replacement and taking all patients of each sampled hospital, so that the
hospital — the level at which the variation of interest arises — is the unit of resampling. Treating
patients as independent would ignore within-hospital correlation and understate the uncertainty.
Standardisation parameters of the pooled model were held fixed across replicates so that only sampling
variation, and not variation in the scale of the predictor, enters the interval. One thousand
replicates were used with the pre-specified random seed (20261019), and the reported interval is the
2.5th to 97.5th percentile of the replicate distribution.

Percentile ranges reported elsewhere in this manuscript — for example the 10th and 90th percentiles
of the per-hospital AUC, observed-to-expected ratio and calibration slope — are **spreads across
hospitals, not confidence intervals**, and are not presented as tests of any hypothesis.

## Software, seed and reproducibility

Analyses were performed in Python 3.14 with pandas 3.0.5, NumPy 2.5.1, scikit-learn 1.9.0, SciPy 1.18.0,
statsmodels 0.14.6, Matplotlib 3.11.0 and DuckDB 1.5.6 (read-only queries against the PhysioNet
catalogue). Exact versions are pinned in `requirements.txt`.

The global random seed was **20261019**; all resampling used explicitly seeded
`numpy.random.Generator` instances with deterministic, derived seeds, so every resampling-based number is
bit-reproducible. Analyses A–D, K are deterministic given the input data. The analysis plans for all
analyses were written before execution and are reproduced in Supplementary Item S1.

The complete analysis and figure-generation code, all derived result files, the prespecified plans, and
this document are publicly archived with a DOI (see Data Availability). Patient-level records are not
redistributed, under the terms of the PhysioNet data use agreements; the centred-level summary table
(103 centres × 3 scores) on which Figures 3–5 depend is included, and contains no patient identifiers,
no dates and no free text.

## Ethics

⟨ETHICS⟩

Required statement structure (BMC/Springer Nature policy):

1. Names the institutional or national research ethics committee that approved the study, with the
   reference number where applicable.
2. States that the study was performed in accordance with the Declaration of Helsinki.
3. If a study was **granted an exemption** from requiring ethics approval, states this **and names the
   committee that granted the exemption**.
4. States that informed consent was obtained, or that it was not required (typically the case for
   secondary analysis of de-identified publicly available data).

Draft once the number is known (placeholders `⟨⟩` to be filled):

> This study is a retrospective secondary analysis of publicly available, de-identified data and does not
> involve identifiable human participants. The use of the eICU Collaborative Research Database and
> MIMIC-IV under their respective PhysioNet data use agreements was reviewed by the ⟨COMMITTEE NAME⟩,
> which determined that formal ethical approval was not required and granted an exemption (⟨REFERENCE
> NUMBER⟩), in accordance with the Declaration of Helsinki. All data are de-identified before release by
> the custodians of both databases, and no identifiable human data were accessed by the authors.

## Use of a large language model

This statement is required by the target journal and must be retained.

> During the preparation of this work the authors used a large language model–based coding assistant
> (OpenCode) in order to draft and debug analysis scripts, to generate figures, and to assist with
> English-language drafting. After using this tool, the authors reviewed and edited the content as needed,
> verified every reported number against the underlying result files, and take full responsibility for the
> content of the publication. No large language model was used as an author, and none satisfies the
> journal's authorship criteria.

## Reporting guidelines

The study is reported in accordance with the STROBE statement [24] and its RECORD extension for
routinely collected health data [25]. TRIPOD was **not** used, because no
prediction model was developed or deployed for clinical use: the pooled model served only as a
measurement instrument for quantifying calibration drift, and the study reports heterogeneity and a
recalibration strategy rather than the performance of a model intended for clinical decision-making.

## Data Availability

This is a retrospective secondary analysis of two publicly available, de-identified critical-care databases.
The eICU Collaborative Research Database (eICU-CRD v2.0) and MIMIC-IV (v3.1) are available from PhysioNet
(https://physionet.org/) to investigators who complete the required training and sign the data use agreement.
Neither database may be redistributed, and no patient-level records are reproduced here.

The complete analysis and figure-generation code, the prespecified analysis plans and their timestamps, all
derived result files, and a centre-level summary table containing no patient identifiers (one row per
eligible centre, for each of the three severity scores) are openly available at
https://github.com/tiantian4634/cross-centre-calibration-drift-icu and archived at Zenodo
(https://doi.org/10.5281/zenodo.23479141). Every number reported in this article can be reproduced from
these materials by an investigator with credentialed access to the two source databases: the analysis
scripts read only locally cached centre-level artefacts and require no database credentials.

All database access during this study was read-only, and no script written for this study modified a database.

---

## References

[1] Vincent, J. L. et al. The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure. *Intensive Care Med.* **22**, 707–710 (1996).
[2] Johnson, A. E. W., Kramer, A. A. & Clifford, G. D. A new severity of illness scale using a subset of Acute Physiology and Chronic Health Evaluation data elements shows comparable predictive accuracy. *Crit. Care Med.* **41**, 1711–1718 (2013).
[3] Le Gall, J. R., Lemeshow, S. & Saulnier, F. A new Simplified Acute Physiology Score (SAPS II) based on a European/North American multicenter study. *JAMA* **270**, 2957–2963 (1994).
[4] Van Calster, B., Nieboer, D., Vergouwe, Y., De Cock, B., Pencina, M. J. & Steyerberg, E. W. A calibration hierarchy for risk models was defined: from utopia to empirical data. *J. Clin. Epidemiol.* **74**, 167–176 (2016).
[5] Van Calster, B., McLernon, D. J., van Smeden, M., Wynants, L. & Bossuyt, P. M. M. Calibration: the Achilles heel of predictive analytics. *BMC Med.* **18**, 88 (2020).
[6] Miao, Q. et al. Miscalibration of lung allocation models leads to inaccurate waitlist mortality predictions. *Am. J. Transplant.* **23**, 245–252 (2023).
[7] Han, K. et al. Detection of calibration drift in clinical prediction models to inform model updating. *J. Biomed. Inform.* **111**, 103611 (2021).
[8] Binuya, M. A. E., Engelhardt, E. G., Schröder, C. P., de Vries, E. G. E. & Braat, C. H. M. Methodological guidance for the evaluation and updating of clinical prediction models: a systematic review. *BMC Med. Res. Methodol.* **22**, 317 (2022).
[9] Ensor, J., Snell, K. I. E., Martin, G. P., Sperrin, M. & Riley, R. D. Individual participant data meta-analysis for external validation, recalibration, and updating of a flexible parametric prognostic model. *Stat. Med.* **40**, 3720–3733 (2021).
[10] Riley, R. D. et al. External validation of prognostic models: what, why, how, when and where? *Clin. Kidney J.* **15**, 469–472 (2022).
[11] Moreno, R. P., Metnitz, P. G. H., Almeida, E., Jordan, B. et al. SAPS 3—From evaluation of the patient to evaluation of the intensive care unit. Part 2: Development of a prognostic model for hospital mortality at ICU admission. *Intensive Care Med.* **31**, 1345–1355 (2005).
[12] Zhang, Z. et al. A novel lifelong machine learning-based method to eliminate calibration drift in clinical prediction models. *Artif. Intell. Med.* **125**, 102256 (2022).
[13] Zhang, Z. et al. Clinical transportability, calibration drift, and local updating of a B-mode ultrasound radiomics-clinical prediction model. *Gland Surg.* **15**, 1274 (2026).
[14] Gehringer, C. K., Martin, G. P., Sperrin, M., Welch, C. & Riley, R. D. How to develop, validate, and update clinical prediction models using multinomial logistic regression. *J. Clin. Epidemiol.* **170**, 114–126 (2024).
[15] Ogero, M. et al. Recalibrating prognostic models to improve predictions of in-hospital child mortality in resource-limited settings. *Paediatr. Perinat. Epidemiol.* **37**, 257–269 (2023).
[16] Schnellinger, E. M. & Yang, W. Comparison of dynamic updating strategies for clinical prediction models. *Diagn. Progn. Res.* **5**, 20 (2021).
[17] Tanner, K. T. & Keogh, R. H. Dynamic updating of clinical survival prediction models in a changing environment. *Diagn. Progn. Res.* **7**, 14 (2023).
[18] Riley, R. D., Debray, T. P. A., Collins, G. S., Archer, L. et al. Minimum sample size for external validation of a clinical prediction model with a binary outcome. *Stat. Med.* **40**, 4230–4251 (2021).
[19] Salluh, J. I. F., Quintairos, A., Dongelmans, D. A., Fujii, T. et al. How to establish and run a national ICU benchmarking registry. *Curr. Opin. Crit. Care* **32**, 523–530 (2026).
[20] Moser, A., Reinikainen, M., Jakob, S. M., Selander, T. A. et al. Mortality prediction in intensive care units including premorbid functional status improved performance and internal validity. *J. Clin. Epidemiol.* **142**, 55–63 (2022).
[21] van Geloven, N. et al. Beyond model development in healthcare AI: post-development robustness, post-deployment monitoring, and lifecycle governance. *Healthcare* **14**, 1459 (2026).
[22] Riley, R. D. et al. Transparent reporting of multivariable prediction models developed or validated using clustered data (TRIPOD-Cluster): explanation and elaboration. *BMJ* **380**, e071058 (2023).
[23] Collins, G. S. et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ* **385**, e078378 (2024).
[24] von Elm, E., Altman, D. G., Egger, M., Pocock, S. J., Gøtzsche, P. C. & Vandenbroucke, J. P. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. *Ann. Intern. Med.* **147**, 573–577 (2007).
[25] Benchimol, E. I., Smeeth, L., Guttmann, A., Harron, K. et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) statement. *PLoS Med.* **12**, e1001885 (2015).
[26] Pollard, T. J., Johnson, A. E. W., Raffa, J. D., Celi, L. A., Mark, R. G. & Badawi, O. The eICU Collaborative Research Database, a freely available multi-center database for critical care research. *Sci. Data* **5**, 180178 (2018).
[27] Johnson, A. E. W. et al. MIMIC-IV, a freely accessible electronic health record dataset. *Sci. Data* **10**, 1 (2023).
[28] Higgins, J. P. T. & Thompson, S. G. Quantifying heterogeneity in a meta-analysis. *Stat. Med.* **21**, 1539–1558 (2002).
[29] DerSimonian, R. & Laird, N. Meta-analysis in clinical trials. *Control. Clin. Trials* **7**, 177–188 (1986).
[30] Veroniki, A. A. et al. Methods to estimate the between-study variance and its uncertainty in meta-analysis. *Res. Synth. Methods* **7**, 55–79 (2016).
[31] Efron, B. & Morris, C. Data analysis using Stein's estimator and its generalizations. *J. Am. Stat. Assoc.* **70**, 311–319 (1975).

---

## Author contributions

**Author contributions.** ⟨逐位作者填写，参照 CRediT 条目：Conceptualisation, Data curation, Formal
analysis, Investigation, Methodology, Software, Validation, Visualisation, Writing – original draft,
Writing – review & editing, Project administration, Supervision, Funding acquisition⟩

## Additional Information

**Competing interests.** ⟨逐位作者声明⟩

**Funding.** This research received no external funding. The article processing charge was covered by
the authors' institution.

---

## Figure legends

**Figure 1**

**Flow of participants from eICU-CRD and MIMIC-IV into the analysis.**
**Left, estimation cohort (eICU-CRD v2.0, 208 hospitals).** 200,859 unit stays → first ICU stay per
patient (139,367) → age ≥65 years (71,734; ages >89 recorded as 90) → ICU length of stay ≥24 h (50,138)
→ medical or medical–surgical ICU (31,307) → exclusion of deaths within 24 h of ICU admission (7)
and of missing hospital outcome status (363) → **analysis cohort of 30,796 patients from 187 hospitals
(3,901 in-hospital deaths, 12.7%)**. A centre was eligible for the between-centre analyses if it
contributed ≥100 patients and ≥10 deaths, leaving **k = 103 centres**.
**Right, external application (MIMIC-IV v3.1).** 94,458 ICU stays → first ICU stay per patient (65,366)
→ age ≥65 years (35,499, age corrected by the difference between admission and anchor year)
→ ICU length of stay ≥24 h (28,607) → first stay in a medical or medical–surgical ICU (8,629)
→ exclusion of deaths within 24 h of ICU admission (35) → **analysis cohort of 8,579 patients
(1,654 in-hospital deaths, 19.3%)**. MIMIC-IV comprises a **single centre** (Beth Israel Deaconess
Medical Center); the eICU-derived model was applied to it **without refitting**.
**Notes.** (i) The exclusion of patients missing all of albumin, height and weight (n = 141 in eICU,
n = 15 in MIMIC-IV) is carried over from the source data-extraction protocol so that cohorts remain
comparable with related work from the same research group. **This study analyses none of albumin,
height or weight**, so the step affects neither the analysis cohort nor any result; it is reported
here only for full transparency about the extraction pipeline. (ii) The threshold of ≥100 patients
and ≥10 deaths per centre was prespecified to permit stable estimation of a calibration intercept
in each centre; centres below the threshold contributed to the pooled model but not to the
centre-level analyses.

**Figure 2**

**Discrimination transports across centres; calibration does not.**
SOFA-based model, 103 eICU centres. Each point is a centre: x = its AUC (discrimination),
y = its observed-to-expected ratio (calibration). The horizontal dashed line marks perfect
calibration (O/E = 1); the dotted vertical line marks the pooled AUC (0.732). Marginal histograms
show each marginal distribution. **Per-centre AUC ranged from 0.649 to 0.812 (a spread of 0.16),
whereas per-centre O/E ranged from 0.69 to 1.54 (a 2.2-fold spread)** — calibration varies far more
than discrimination. Point colour encodes $a_h$ (blue < 0, red > 0).

**Figure 3**

**Between-centre drift in calibration intercept for three acute-severity scores.**
Each panel shows one severity score fitted as a single-predictor logistic model on the full eICU-CRD
cohort (30,796 patients; 3,901 in-hospital deaths) and then applied to each of **103 centres**
(≥100 patients and ≥10 deaths). Points are centres sorted by their calibration-in-the-large offset
$a_h$ (solving $\mathrm{mean}\{\mathrm{expit}(\mathrm{logit}(\hat p)+a_h)\}=\mathrm{observed\ mortality}$);
**$a_h > 0$ indicates more deaths than the model predicts**. Bars are 95% CIs (delta method);
point size is proportional to $\log(n)$. Colour encodes $a_h$ (blue = lower than predicted,
red = higher). Heterogeneity ($I^2$) was estimated by random-effects meta-analysis
(DerSimonian–Laird). Between-centre $I^2$ exceeded 70% for all three scores
(SOFA 75.4%, OASIS 79.8%, SAPS-II 70.4%), with observed-to-expected (O/E) ratios spanning
approximately 2.2-fold across centres (P10–P90: 0.69–1.54 for SOFA).
**The drift is therefore a property of the setting rather than of any one score.**

**Figure 4**

**(a)** Between-centre heterogeneity by centre size. Centres were split into tertiles by
sample size; bars are $I^2$ and the orange line is the between-centre variance $\tau^2$.
Heterogeneity **increased** with centre size (small: $I^2$ 56.7%, $\tau^2$ 0.093;
medium: 69.8%, 0.117; large: 83.9%, 0.143). Had the apparent drift been driven by sampling
noise, the least precisely estimated (small) centres would have shown the greatest heterogeneity;
the opposite was observed, indicating that the between-centre variation is real.
**(b)** Clinical impact of the same decision threshold in different centres. For each threshold
$p_t$, points are the median and bars the P10–P90 range of the observed mortality among patients
the model classified as high risk (112 centres with ≥100 patients); the red dashed line is the
overall cohort mortality (12.7%). At $p_t$ = 0.20 the observed mortality among flagged patients
ranged from **15% to 52% (3.5-fold)**. Model-guided escalation yielded **negative net benefit in
6.2%, 17.0%, 21.4% and 22.3% of centres** at $p_t$ = 0.10, 0.20, 0.30 and 0.40 respectively —
i.e. in up to one in five centres the model performed worse than treating everyone.

**Figure 5**

**(a)** Learning-curve analysis: for each $m$, $m$ patients per centre were drawn for local recalibration and the remainder for evaluation ($n\ge 2m$; 100 repeats per centre-$m$ cell). y axis: proportion of attempts with residual O/E within ±10% for S1 (intercept only) and S2 (intercept + slope); dotted line, no recalibration; dashed line, the 50% target; k, the number of contributing centres. **With 25 local patients, naive recalibration was worse than no recalibration at all (21.4% → 15.3%); the 50% target was never reached.**
**(b)** Residual miscalibration |$a$| (median; band → P90).
**(c)** Empirical-Bayes (EB) shrinkage removes the penalty: 103 centres; 200 paired resamples per centre-$m$ cell; $\bar a$ and per-centre SEs were leave-one-centre-out cross-fitted, so no centre's evaluation data entered its own shrinkage parameters. S0, no recalibration; S1/S2, naive; S3, EB shrinkage, $\hat a_{\mathrm{EB}}=\bar a+\lambda(\hat a_{\mathrm{ML}}-\bar a)$, $\lambda=\tau^2/(\tau^2+\mathrm{SE}^2)$. At $m$ = 25 the success rate rose from 15.5% to 24.3% (paired difference +9.05 percentage points, Wilcoxon P = 3.7×10⁻¹¹²), surpassing no recalibration (21.4%); median $\lambda$ 0.234/0.374/0.536/0.712 (m = 25/50/100/200), and residual |$a$| fell from 0.44 (naive) to 0.26.
**(d)** Shrinkage parameters estimated once from eICU transfer to a different database: MIMIC-IV treated as a single new centre; $\bar a$ = +0.030 and $\tau^2$ = 0.131 fixed from eICU, never re-estimated; the offset to recover, $a^*$ = +0.221. EB shrinkage outperformed naive recalibration at every $m$ (at $m$ = 25: 47.0% vs 23.5%, +23.5 percentage points, Wilcoxon P = 6.3×10⁻⁷); **25 patients with shrinkage matched the success rate naive recalibration reached only with roughly 150 patients — a six-fold smaller local sample requirement.**
**Notes.** The contributing-centre set shrinks with $m$; the S0 line is the *within-m* benchmark (not a learning effect). Panels a–b use 100 resampling attempts (15.3% at $m$ = 25), panels c–d 200 paired attempts (15.5%); both are correct independent draws — comparisons are within, not between, panels. MIMIC-IV is a single-centre database: panel d tests whether the shrinkage parameters transfer across databases and does not constitute multicentre external validation, which can only be evaluated within eICU itself (panel c). The dip at $m$ = 50 (panel d) is Monte-Carlo variation across the 200 attempts; read the trend across the panel.

---

## Table 1

**Table 1. Between-centre variation in discrimination and calibration across 103 intensive-care
units, by severity score**

| | SOFA | OASIS | SAPS-II |
|---|---|---|---|
| Hospitals included, *k* | 103 | 103 | 103 |
| Pooled model AUC (95% CI) | 0.732 (0.720–0.745) | 0.728 (0.715–0.741) | 0.761 (0.751–0.771) |
| Per-centre AUC, 10th / median / 90th percentile | 0.649 / 0.738 / 0.812 | 0.666 / 0.729 / 0.813 | 0.683 / 0.762 / 0.844 |
| Between-centre variance (τ²) | 0.131 | 0.165 | 0.109 |
| Between-centre heterogeneity (I²), % | 75.4 | 79.8 | 70.4 |
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