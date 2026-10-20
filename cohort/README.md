# Cohort construction

This folder documents how the two analysis cohorts were built from the raw PhysioNet tables, and contains
the **step-wise count reports emitted by the extraction stage** (`eicu_counts.json`, `mimic_counts.json`).
Those count reports — not a later reconstruction — are the source of every number in Figure 1.

The extraction itself requires credentialed PhysioNet access and is therefore **not re-run as part of this
repository**. Patient-level derived files are excluded by `.gitignore` under the PhysioNet data use
agreement.

---

## eICU-CRD v2.0 → 30,796 patients in 187 hospitals

| Step | Criterion | n remaining |
|---|---|---|
| 0 | all unit stays in the database (208 hospitals) | 200,859 |
| 1 | first ICU stay per patient (ordered by hospital admission time within `uniquepid`) | 139,367 |
| 2 | age ≥ 65 years (the `age` field records `> 89`; converted to 90; empty strings excluded) | 71,734 |
| 3 | ICU length of stay ≥ 24 h (`unitdischargeoffset` ≥ 1440 min) | 50,138 |
| 4 | unit type is `MICU` or `Med-Surg ICU` | 31,307 |
| 5 | *exclude* death within 24 h of ICU admission | 31,300 (−7) |
| 6 | *exclude* missing hospital outcome status (`hospitaldischargestatus` not in {expired, alive}) | 30,937 (−363) |
| 7 | *exclude* albumin, height and weight all missing | **30,796** (−141) |
| | **analysis cohort** | **30,796** (3,901 deaths, 12.7%) |

Of the 187 hospitals contributing, **103 met ≥ 100 patients and ≥ 10 deaths** and entered the
centre-level analyses. Centres below the threshold still contributed to the pooled model.

**Note on step 7.** This exclusion is carried over from the source data-extraction protocol so that cohorts
remain comparable with related work from the same research group. This study analyses neither albumin,
height nor weight, so the step affects neither the analysis cohort nor any result. It is reported in
Figure 1 and in the supplementary notes for transparency about the extraction pipeline.

## Temporal split-half eligibility

eICU-CRD covers only 2014–2015. Of the 103 centres eligible for centre-level analysis, **88 contributed
≥ 50 patients and ≥ 5 deaths in each of the two calendar years** and entered the within-hospital temporal
stability analysis. Per-centre calibration offsets and standard errors for each year, together with the
year-over-year difference, are in `03_统计/temporal_split_half.csv` (88 rows). This analysis addresses
year-to-year stability only; two years cannot support a claim about longer-term temporal trend.

## MIMIC-IV v3.1 → 8,579 patients, single centre

| Step | Criterion | n remaining |
|---|---|---|
| 0 | all ICU stays | 94,458 |
| 1 | first ICU stay per patient | 65,366 |
| 2 | age ≥ 65 years (`anchor_age`, corrected by the difference between admission year and anchor year) | 35,499 |
| 3 | ICU length of stay ≥ 24 h (`los` ≥ 1) | 28,607 |
| 4 | first stay in `Medical Intensive Care Unit (MICU)` or `Medical/Surgical Intensive Care Unit (MICU/SICU)` | 8,629 |
| 5 | *exclude* death within 24 h of ICU admission | 8,594 (−35) |
| 6 | *exclude* albumin, height and weight all missing | **8,579** (−15) |
| | **analysis cohort** | **8,579** (1,654 deaths, 19.3%) |

MIMIC-IV comprises a **single centre** (Beth Israel Deaconess Medical Center). The eICU-derived model was
applied to it without refitting.

---

## Reproducing this step

With credentialed access to the PhysioNet tables, the extraction follows the criteria above in the order
listed. The step-wise counts it emits should reproduce the two JSON files in this folder exactly; any
discrepancy would indicate a change in database version or in the source protocol.

Variables required beyond the counts: `patient` (eICU: `uniquepid`, `patientunitstayid`, `hospitalid`,
`age`, `unitdischargeoffset`, `unittype`, `hospitaldischargestatus`, `hospitaldischargeoffset`,
`hospitaladmitoffset`); `icustays`, `admissions`, `patients` (MIMIC-IV: `first_careunit`, `los`,
`anchor_age`, `anchor_year`, `intime`, `deathtime`); and the severity components needed to compute SOFA,
OASIS and SAPS-II.

Severity scores are used as supplied by the source extraction; the study does not recompute them, and
their derivation is documented in the source protocol.
