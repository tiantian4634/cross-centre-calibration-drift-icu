# Cross-centre calibration drift of acute severity scores

**Companion code for:** *Discrimination transports, calibration does not: cross-centre and temporal drift in
acute severity scoring across 187 ICUs, and the sample size needed to recalibrate*

---

## The short version

When a prediction model is developed in one hospital and used in another, its **discrimination** (how well
it ranks patients) often travels. Its **calibration** (whether the predicted risks match the observed
risks) frequently does not.

Working in 103 intensive-care units from the eICU Collaborative Research Database, we found that a
SOFA-based model's AUC ranged only from 0.649 to 0.812 across centres — while the observed-to-expected
mortality ratio ranged from 0.69 to 1.54, a 2.2-fold spread. The pattern held for OASIS and SAPS-II, was
not explained by measured case-mix, and grew with centre size rather than shrinking, so it is not a
small-sample artefact. Splitting centres by calendar year showed the calibration offset is itself unstable
year to year (r = 0.59; 42% of the between-centre variance is temporal).

The practical consequence is uncomfortable: **naive centre-by-centre recalibration is not the fix it is
usually assumed to be.** With only 25 local patients it makes calibration *worse* than doing nothing. It
needs hundreds of patients, and even at 200 the success rate is 34%.

Applying empirical-Bayes shrinkage — shrinking each centre's estimated offset toward the pooled mean, with
the shrinkage weight set by the between-centre variance — reverses this. At 25 local patients it outperforms
both naive recalibration and no recalibration at all, and performs comparably to naive recalibration with
roughly eight times as many patients. The shrinkage parameters estimated once from eICU transfer to
MIMIC-IV without refitting.

---

## Data access

The analysis uses two credentialed PhysioNet databases. **No patient-level data is redistributed here.**

| Database | Version | Access |
|---|---|---|
| eICU Collaborative Research Database | v2.0 | PhysioNet — training plus a data use agreement |
| MIMIC-IV | v3.1 | PhysioNet — CITI "Data or Specimens Only" training plus a DUA |

Request access at [physionet.org](https://physionet.org/). Application is free but takes several weeks.

---

## Running the analysis

Only the first step needs database credentials. Everything afterwards reads local files.

```bash
pip install -r requirements.txt

# Step 0 — one-off: cache centre-level fields so later steps need no database access
#   (edit DB_PATH below to point at your local PhysioNet DuckDB catalogue)
python extract_hospital_context.py

# Step 1 — feasibility probe
python roadB_probe.py

# Steps 2-8 — the analysis pipeline, in order
python analysis_drift.py
python analysis_learning_curve.py
python analysis_batch2.py
python analysis_shrinkage.py
python analysis_mimic_external.py
python analysis_tau2_framework.py
python analysis_tau2_sensitivity.py

# Figures
python figure1_flowchart.py
python figures_drift.py
python figures_batch2.py
python figures_shrinkage.py
python figures_mimic_external.py
```

**Determinism.** The global seed is `20261019`; resampling uses explicitly seeded
`numpy.random.Generator` instances, so every resampling-based number is bit-reproducible.

**Database access is read-only.** No script writes to a database.

**Plan files are never overwritten.** Each analysis plan is written idempotently — once present, a
re-run leaves it untouched — so that the file timestamps continue to evidence that the analyses were
specified before they were run.

**Local paths.** The scripts contain hard-coded absolute paths to the machine on which the analysis was
run (`E:\…` for the working directory, `F:\…` for the PhysioNet DuckDB catalogue). These are **not** a
disclosure risk, but you must edit them to match your own layout. The names to change are `BASE`,
`SRCDIR`, `ST`, `FG` and `DB_PATH` near the top of each script.

**What a reader without PhysioNet access can verify.** Because the cohort is derived from credentialed
data that cannot be redistributed, the analysis cannot be re-run end to end without access. A reader can
nevertheless check the centre-level results directly from `03_统计/hospital_level_三评分.csv`
(309 rows = 103 centres × 3 scores), which contains every quantity plotted in Figures 3, 4 and 5.

---

## Repository layout

```
extract_hospital_context.py        cache centre-level fields (needs PhysioNet access)
roadB_probe.py                     feasibility probe: heterogeneity across centre-size thresholds
analysis_drift.py                  analyses A-D: drift, slopes, case-mix ladder, MIMIC positioning
analysis_learning_curve.py         analysis E: local recalibration learning curve
analysis_batch2.py                 analyses F-H: temporal stability, size strata, clinical impact
analysis_shrinkage.py              analysis I: empirical-Bayes shrinkage vs naive recalibration
analysis_mimic_external.py         analysis J: transfer of shrinkage parameters to MIMIC-IV
analysis_tau2_framework.py         analysis K: tau^2 under four estimation frameworks
analysis_tau2_sensitivity.py       sensitivity of the main conclusion to the choice of tau^2
diagnose_multilevel.py             diagnostics for the multilevel estimator
verify_vcp_parameterization.py     diagnostics resolving a statsmodels parameterisation question

figure1_flowchart.py               Figure 1
figures_drift.py                   Figures 3-6
figures_batch2.py                  Figures 8-9
figures_shrinkage.py               Figure 10
figures_mimic_external.py          Figure 11

03_统计/                           all result tables, heterogeneity estimates, resampling outputs
04_图表/                           figures (PNG 600 dpi + PDF)
07_投稿附件/                       data & code availability statements; Supplementary Item S1
```

## Analysis plans

Every analysis was specified in a written plan **before** it was run, each stating its design and, where
applicable, an explicit criterion together with an instruction for the case where that criterion was not
met. The plans are reproduced verbatim in `07_投稿附件/S1_分析计划汇总与披露.md` (Supplementary Item S1),
together with file timestamps, an English summary of each plan, a classification of analyses into
descriptive versus confirmatory tiers, and a disclosure of one file-timestamp defect.

**Two of the four pre-specified criteria were not met and are reported as negative findings** — they were
not reframed after the fact.

---

## Citation

If you use this code or the accompanying results, please cite the manuscript above. A BibTeX entry will be
added once the record is finalised.

## Licence

Code: MIT. Documentation and figures: CC BY 4.0. Neither applies to PhysioNet data, which is governed by
its own data use agreement.
