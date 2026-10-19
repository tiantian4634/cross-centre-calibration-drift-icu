# Methods —— Scientific Reports 投稿版

> 目标期刊：Scientific Reports。该刊**不限 Methods 字数**，要求"足以让他人复现"。
> 本文所有数字均来自 `结果汇总_v1.md`（唯一权威来源）与 `cohort\` 的逐步计数。
>
> **占位符**：`⟨ETHICS⟩` = 伦理委员会名称 + 批件号（**用户提供**）；
> `⟨⟨FULL⟩⟩` = 该节为完整正文，非占位。

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

**eICU-CRD v2.0**[20] contains data from 208 hospitals in the United States for the period 2014–2015,
comprising 200,859 intensive-care unit (ICU) stays. Access required credentialed application and
attestation of the PhysioNet data use agreement.

**MIMIC-IV v3.1**[21] contains data from Beth Israel Deaconess Medical Center, a single academic medical
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
Organ Failure Assessment (SOFA)[18], the Oxford Acute Severity of Illness Score (OASIS), and the Simplified
Acute Physiology Score II (SAPS-II)[19]. This study did not recompute the scores, and their derivation is
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
respectively) were all specified in the analysis plans written before execution (Supplementary Note
S1).

## Between-centre heterogeneity

For each score, per-hospital offsets were pooled by random-effects meta-analysis. Heterogeneity was
summarised by *I²*, defined as `max(0, (Q − (k − 1))/Q) × 100`, where *Q* is the fixed-effect
Cochran statistic computed with weights 1/SE². The between-centre variance *τ²* was estimated by the
DerSimonian–Laird method[22]. Because DerSimonian–Laird predates current guidance, *τ²* was additionally
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
|Δa_h|, the ratio of within-hospital (temporal) variance to total between-hospital variance, and the
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
calibration slope; and **S3**, empirical-Bayes shrinkage of the intercept

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
SOFA pooled model, applied using eICU's standardisation parameters. The true offset to recover, *a*\* =
+0.221, was computed once from the full MIMIC-IV cohort (observed 19.3% versus predicted 16.5%,
O/E = 1.17). For each *m* ∈ {25, 50, 100, 200, 400} subject to *n* ≥ 2*m*, *m* patients were drawn as
the local calibration set and the remainder served as evaluation, **200 times per cell**, with the same
seed construction as above.

**This analysis tests whether the shrinkage parameters transfer across databases. It is not
multicentre external validation of the strategy**, which can only be evaluated within eICU itself
(analysis I). The two are reported separately throughout and are not conflated.

## Analysis framework and inferential status

*(This block is taken from `07_投稿附件/Methods_分析层级与推断地位.md` and is intentionally reproduced
here so that the two are kept in sync.)*

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

| Analysis | Pre-specified criterion | Criterion met? |
|---|---|---|
| E — local recalibration learning curve | Report the smallest local sample size *m* at which the success rate reaches 50%; if none is reached, state so | **No** — never reached within m = 200 |
| I — empirical-Bayes shrinkage vs naive | At m = 25 the shrinkage strategy must exceed naive recalibration; at m ≥ 100 it must not be worse by more than 5 percentage points | **Yes** |
| J — transfer of shrinkage parameters to a second database | At m = 25 shrinkage must exceed both naive recalibration and no recalibration | **Yes** |
| K — agreement of *τ²* across estimation frameworks | Relative range across the three two-stage estimators < 25%, and the one-stage multilevel estimate within 50% of their median | **Partly** — first clause met (3.9%), second clause **not** met (multilevel *τ²* 50.1% lower) |

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
this document are publicly archived with a DOI (see Data availability). Patient-level records are not
redistributed, under the terms of the PhysioNet data use agreements; the centred-level summary table
(103 centres × 3 scores) on which Figures 3–5 depend is included, and contains no patient identifiers,
no dates and no free text.

## Ethics

⟨ETHICS⟩ **【占位——须由用户提供：伦理委员会全称 + 批件号/豁免认定文号】**

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

**【写作时须由作者核对措辞】** —— 如实际使用范围与上述不符（例如某一部分完全是本人手写），请据实
缩窄描述。**宁可低估，不可高估。**

## Reporting guidelines

The study is reported in accordance with the STROBE statement. TRIPOD was **not** used, because no
prediction model was developed or deployed for clinical use: the pooled model served only as a
measurement instrument for quantifying calibration drift, and the study reports heterogeneity and a
recalibration strategy rather than the performance of a model intended for clinical decision-making.

## Data availability

*(正文末尾、References 之前，Sci Rep 标为 mandatory。材料已备于
`07_投稿附件/Data_Code_Availability.md`，投稿前须翻译成该刊所需段落并填入 Zenodo DOI。)*

---

## 本节完成后的自查清单

- [ ] `⟨ETHICS⟩` 已替换为真实委员会名称 + 批件号
- [ ] LLM 声明措辞经作者本人核对
- [ ] 每处 P 值在 **Results** 中都带检验名/n/α/单双尾（Methods 已给出规则）
- [ ] Data availability 已翻译成投稿段落并含 Zenodo DOI
- [ ] 与 `Methods_分析层级与推断地位.md` 保持同步（两处改动须同改）
- [ ] 未出现三条措辞红线的违规表述