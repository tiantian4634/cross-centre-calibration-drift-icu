# Structured Abstract — 投稿版

**Journal-ready abstract · word count ≈ 410 · 结构：Background / Methods / Results / Conclusions**

占位符：`⟨ethics⟩` 伦理声明句｜`⟨JOURNAL⟩` 目标期刊｜`⟨JOURNAL⟩` 用于 STROBE 声明位置

---

## Abstract

**Background.** Acute severity scores are widely assumed to be transportable between hospitals.
We examined whether the discrimination and the calibration of such scores remain comparable
across centres, and how many local patients a valid recalibration actually requires.

**Methods.** We performed a retrospective secondary analysis of the eICU Collaborative Research
Database (30,796 patients aged ≥65 years from 187 hospitals, of whom 3,901 died [12.7%]; 103
centres with ≥100 patients and ≥10 deaths eligible for centre-level analysis) and of MIMIC-IV
(8,579 patients, one centre). We fitted pooled logistic models for SOFA, OASIS and SAPS-II and
derived for each centre the observed-to-expected (O/E) mortality ratio, the calibration-in-the-large
offset and the calibration slope. Between-centre heterogeneity was estimated by random-effects
meta-analysis (DerSimonian-Laird) and cross-checked under Paule-Mandel, REML and a one-stage
multilevel logistic model. Local recalibration was evaluated by repeated resampling (100
repetitions per centre), against a success criterion of |O/E − 1| ≤ 10%. We additionally examined
empirical-Bayes shrinkage of each centre's calibration offset toward the pooled mean, with the
shrinkage target and variance estimated by leave-one-centre-out cross-fitting. All analysis plans
were written before execution; four analyses carried pre-specified criteria, **of which two were
not met and are reported as such**.

**Results.** Pooled discrimination was moderate (AUC 0.732 SOFA, 0.728 OASIS, 0.761 SAPS-II) and
barely varied between centres (AUC 0.649–0.812). Calibration varied substantially: I² was 75.4%,
79.8% and 70.4%, and the O/E ratio ranged from 0.69 to 1.54, a 2.2-fold spread. Calibration slopes
ranged from 0.72 to 1.64, indicating drift in the risk gradient itself. Drift was not explained by
measured case-mix (adding age, sex, comorbidity and ventilation raised AUC by 0.020 but reduced
I² by only 5 percentage points), strengthened with centre size (τ² 0.093 → 0.143 from smallest to
largest tertile) and was temporally unstable within centres (split-half r = 0.586; 41.6% of the
apparent between-centre variance was temporal). Clinically, at a decision threshold of 0.20 the
observed mortality among patients flagged high-risk ranged from 15% to 52%, and net benefit was
negative in 17–22% of centres. Naive local recalibration carried a small-sample penalty: with 25
local patients it performed *worse* than no recalibration at all (success rate 15.5% versus
21.4%), and even at 200 patients only 34.3% of resamples met the criterion — the pre-specified
50% threshold was never reached. Empirical-Bayes shrinkage reversed this. At 25 local patients it
achieved a 23.4% success rate versus 15.5% for naive recalibration (paired difference +8.2
percentage points, P = 2.5 × 10⁻⁹²), with the shrinkage weight adapting to sample size
(median λ = 0.234). Fixing the shrinkage parameters on eICU and transferring them unchanged to
MIMIC-IV treated as a single new centre yielded 53.5% versus 23.5% at 25 patients
(+30.0 points, P = 7.4 × 10⁻¹³), equivalent to naive recalibration with about 200 patients. The
two-stage τ² estimates agreed closely (relative range 3.9%) but the one-stage multilevel estimate
was 50% lower — a pre-specified disagreement that did not alter any conclusion.

**Conclusions.** Discrimination transports; calibration does not. Drift of this magnitude is
neither explained by measured case-mix nor attributable to small-sample noise, and it changes what
a risk threshold means at the bedside. Naive centre-by-centre recalibration is not the remedy it is
commonly assumed to be. Shrinking the local calibration offset toward the pooled mean makes local
recalibration worthwhile at a sample size where naive recalibration is harmful, and the shrinkage
parameters transferred to a second database without refitting. This is a statistical
recalibration strategy, not a clinical recommendation.

**Keywords.** Intensive care; severity score; calibration; external validation; data drift;
empirical Bayes; SOFA; OASIS; SAPS-II; eICU; MIMIC-IV

---

## 写作说明（不进正文）

**必须保留的三处「诚实表述」**——删掉任何一处都会削弱稿件可信度，且可能被审稿人当作选择性报告：

1. `of which two were not met and are reported as such`
2. `the pre-specified 50% threshold was never reached`
3. `a pre-specified disagreement that did not alter any conclusion`

**三条措辞红线已全部落实**，摘要中未出现任何归因于医疗质量的表述：

- 漂移一律称 between-centre variation / drift，未称「质量差异」
- MIMIC 部分写 `treated as a single new centre`，未称「外部多中心验证」
- 结论末句明确 `a statistical recalibration strategy, not a clinical recommendation`

**待填**：伦理声明句（须含伦理委员会名称与批件号）、STROBE 声明位置（按目标期刊要求放在 Methods 末或投稿系统）。