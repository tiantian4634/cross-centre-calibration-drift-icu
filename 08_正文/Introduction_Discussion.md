# Introduction & Discussion —— Scientific Reports 投稿版

> **Sci Rep 结构要求**：Introduction、Results（带小标题）、Discussion（**不带小标题**）、Methods。
> 三者合计 ≤ 4,500 词（不含摘要、Methods、参考文献、图注）。
> 参考文献采用 Nature 格式（方括号数字序），≤ 60 条（建议值）。
>
> **红线自查**：本文件不得出现「质量差异」「医疗质量」「外部多中心验证」的肯定性表述；
> 结论须含「statistical recalibration strategy, not a clinical recommendation」。

---

## Introduction

Acute severity scores such as the Sequential Organ Failure Assessment (SOFA), the Oxford Acute
Severity of Illness Score (OASIS) and the Simplified Acute Physiology Score II (SAPS-II) are used
across intensive care units (ICUs) to quantify illness severity, to benchmark units against one
another, and increasingly to inform decisions about the level of care a patient should receive.
Their use rests on an assumption that is rarely examined: that a given score means the same thing
about the probability of death in one hospital as it does in another.

Discrimination is the property that is usually reported. A score that ranks sicker patients above
healthier ones will retain most of that ability when it is carried from one population to another,
and a pooled area under the receiver operating characteristic curve (AUC) is a standard feature of
validation studies. Calibration — whether the predicted probability of death matches the observed
probability — is the property that determines what a risk estimate actually means at the bedside,
and it has long been recognised as the more fragile of the two. Poorly calibrated algorithms can be
misleading and harmful in clinical decision-making, and calibration has been described as the
Achilles heel of predictive analytics [1]. Even so, calibration is assessed less consistently than
discrimination in published validation studies [2], and where it is assessed the finding is
typically that it does not transport.

Most published work on calibration failure addresses one of two settings. The first is temporal:
within a single environment, calibration deteriorates as clinical practice, data capture and
patient mix change, and a substantial methodological literature now exists on detecting such drift
[3] and on updating models once it has been detected [4,5]. The second is a single transfer: a model
developed in one centre is applied to one other centre or population, where miscalibration is
observed and locally corrected [6]. What has received much less attention is the *spatial*
dimension — how far calibration differs **simultaneously across many centres** in a health system
that routinely uses the same score, and how large that between-centre component is relative to the
others. This matters because the practical response to inter-centre variation is assumed to be
local recalibration, and because benchmarking systems that compare hospitals depend on the premise
that the underlying risk adjustment is comparable across them.

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
[3], and Zhang et al. proposed lifelong machine learning to counter it across four tumour datasets
[7]. Both are well-suited to their question and neither is contradicted here. The present study
addresses the orthogonal question — the *spatial* component — and does so at a scale rarely
attempted: rather than one environment followed over time or one transfer from centre to centre
[6,8], we observed 103 centres simultaneously and were able to partition the resulting variance. A
clinically important corollary is that the two sources are not interchangeable. A hospital offset
that is 41.6% temporal in origin cannot be fixed by a permanent recalibration, however large the
sample used to fit it, and a hospital-to-hospital difference that persists after case-mix adjustment
cannot be explained by improvement over time. Decomposing them would require a database spanning
several years, which eICU-CRD does not.

**Relation to the model-updating literature.** A mature methodological literature describes how to
evaluate and update a prediction model, including when recalibration is appropriate [4,5,9,10], and
empirical comparisons of update strategies exist [11,12]. Those recommendations are generally
presented as unqualified: if calibration in the target setting is poor, recalibrate. Our findings
qualify rather than contradict them. The literature assumes a local sample large enough for the
recalibration to be estimated reliably, and does not typically state what that means in patients. We
found that with 25 local patients naive recalibration lowered the proportion of resamples reaching
±10% accuracy from 21.4% to 15.3%, that estimating a second parameter (the calibration slope) made it
worse still, and that a 50% success rate was not reached even at 200 patients. The quantity the
guidance leaves unspecified — how many local patients — appears to be the parameter that governs
whether the recommendation helps.

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
[13,14], and such systems presume that observed-to-expected ratios are comparable between
institutions. Our results indicate that this premise requires active verification: an observed-to-
expected ratio of 0.69 in one hospital and 1.54 in another, under the same model, is not a
difference in performance that a benchmark can safely interpret. Because the variation is only
partly temporal and not explained by measured case-mix, neither a stable unit-level adjustment nor a
one-off recalibration resolves it. The emerging focus on post-deployment monitoring and lifecycle
governance of clinical models [15] would be strengthened by treating centre-specific calibration as
a quantity to be monitored rather than assumed.

**Why STROBE rather than TRIPOD.** The data are clustered by hospital, which is the structure the
TRIPOD-Cluster statement was written to address [16], and reporting standards for prediction models
have continued to develop with TRIPOD+AI [17]. We report using STROBE because no prediction model
was developed or deployed for clinical use in this study: the pooled model served as a measurement
instrument for quantifying drift, and the object of the study is the between-centre variation
itself, not the performance of a model intended for patient-level decisions. We have nonetheless
reported the elements that matter for clustered data — the clustering level, the number of centres
per estimate, and the resampling design.

**Limitations.** First, eICU-CRD covers only 2014 and 2015. This study therefore quantifies the
spatial component of drift and provides no evidence about longer-term temporal trends; the
year-to-year analysis reported here addresses stability across two consecutive years and nothing
more. Second, MIMIC-IV is a single centre, so the external analysis tests whether the shrinkage
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