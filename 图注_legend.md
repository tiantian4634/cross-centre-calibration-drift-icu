# 跨中心校准漂移研究 · 图注（Legends）合集

生成：2026-10-19（B）
用途：SCI 投稿用**英文图注（正文/投稿系统用）** + 中文对照（自己与导师核对用）。

---

## ⚠️ 版式约定（务必遵守）

图内**不出现**主标题、解释性副标题、底部文字注释——这些信息**全部写在本文件的图注里**。
图内只保留：面板标识、坐标轴标签、图例、图内统计标注框。

**被从图上删掉、但必须保留在图注里的关键声明**（Supplementary Fig. S1 与 Fig. 4）：
> 「实测病例组合解释不了漂移」「残余院间变异不作医疗质量归因」——
> 这是**方法学红线**，删掉图注就等于丢了这条声明，审稿人会追问。

> **编号说明**（2026-10-21 重排）：图号已按**投稿正文首现顺序**统一：
> Figure 1 = 两库筛选流程图；Figure 2 = 判别稳与校准漂（散点图）；Figure 3 = 三评分校准漂移对比（caterpillar）；
> Figure 4 = 规模分层与临床影响；Figure 5 = 重校准与收缩收益（**合并原"学习曲线 + 分层收缩 + MIMIC 迁移"三图**，四面板 a–d）；
> Supplementary Fig. S1–S3 不变。小节物理顺序与编号无关，装配时按编号排序提取。

---

# Figure 1

### English legend

> **Flow of participants from eICU-CRD and MIMIC-IV into the analysis.**
> **Left, estimation cohort (eICU-CRD v2.0, 208 hospitals).** 200,859 unit stays → first ICU stay per
> patient (139,367) → age ≥65 years (71,734; ages >89 recorded as 90) → ICU length of stay ≥24 h (50,138)
> → medical or medical–surgical ICU (31,307) → exclusion of deaths within 24 h of ICU admission (7)
> and of missing hospital outcome status (363) → **analysis cohort of 30,796 patients from 187 hospitals
> (3,901 in-hospital deaths, 12.7%)**. A centre was eligible for the between-centre analyses if it
> contributed ≥100 patients and ≥10 deaths, leaving **k = 103 centres**.
>
> **Right, external application (MIMIC-IV v3.1).** 94,458 ICU stays → first ICU stay per patient (65,366)
> → age ≥65 years (35,499, age corrected by the difference between admission and anchor year)
> → ICU length of stay ≥24 h (28,607) → first stay in a medical or medical–surgical ICU (8,629)
> → exclusion of deaths within 24 h of ICU admission (35) → **analysis cohort of 8,579 patients
> (1,654 in-hospital deaths, 19.3%)**. MIMIC-IV comprises a **single centre** (Beth Israel Deaconess
> Medical Center); the eICU-derived model was applied to it **without refitting**.
>
> **Notes.** (i) The exclusion of patients missing all of albumin, height and weight (n = 141 in eICU,
> n = 15 in MIMIC-IV) is carried over from the source data-extraction protocol so that cohorts remain
> comparable with related work from the same research group. **This study analyses none of albumin,
> height or weight**, so the step affects neither the analysis cohort nor any result; it is reported
> here only for full transparency about the extraction pipeline. (ii) The threshold of ≥100 patients
> and ≥10 deaths per centre was prespecified to permit stable estimation of a calibration intercept
> in each centre; centres below the threshold contributed to the pooled model but not to the
> centre-level analyses.

### 中文对照

> **图1　eICU-CRD 与 MIMIC-IV 进入分析的筛选流程。**
> **左，估计队列（eICU-CRD v2.0，208 家医院）**：200,859 unit stays → 首次 ICU 入住（139,367）
> → ≥65 岁（71,734，>89 岁记为 90）→ ICU 停留 ≥24 h（50,138）→ 内科或内外科 ICU（31,307）
> → 排除入 ICU 24 h 内死亡（7）与院内结局状态缺失（363）→ **分析队列 30,796 例，187 家医院
> （死亡 3,901 例，12.7%）**。中心需 ≥100 例且 ≥10 例死亡方可进入院间分析，**最终 k = 103 家中心**。
>
> **右，外部应用（MIMIC-IV v3.1）**：94,458 → 65,366 → ≥65 岁（35,499）→ ICU ≥24 h（28,607）
> → 内科/内外科 ICU 首次入住（8,629）→ 排除 24 h 内死亡（35）→ **分析队列 8,579 例（死亡 1,654 例，19.3%）**。
> MIMIC-IV 为**单中心**（BIDMC），eICU 推导的模型**不经重新拟合**直接应用。
>
> **说明**：(i)「白蛋白/身高/体重全缺失者排除」（eICU 141 例、MIMIC 15 例）沿用同一研究组前序数据提取方案，
> 以保持与相关研究队列的可比性。**本研究不使用上述任何变量**，该步骤既不影响分析队列也不影响任何结果，
> 此处列出仅为完整交代提取流程。(ii)「≥100 例且 ≥10 例死亡」的阈值系**预先设定**，用于保证每家中心的
> 校准截距可稳定估计；未达阈值的中心仍进入合并模型，但不参与中心层面分析。

---
# Figure 3

### English legend

> **Between-centre drift in calibration intercept for three acute-severity scores.**
> Each panel shows one severity score fitted as a single-predictor logistic model on the full eICU-CRD
> cohort (30,796 patients; 3,901 in-hospital deaths) and then applied to each of **103 centres**
> (≥100 patients and ≥10 deaths). Points are centres sorted by their calibration-in-the-large offset
> $a_h$ (solving $\mathrm{mean}\{\mathrm{expit}(\mathrm{logit}(\hat p)+a_h)\}=\mathrm{observed\ mortality}$);
> **$a_h > 0$ indicates more deaths than the model predicts**. Bars are 95% CIs (delta method);
> point size is proportional to $\log(n)$. Colour encodes $a_h$ (blue = lower than predicted,
> red = higher). Heterogeneity ($I^2$) was estimated by random-effects meta-analysis
> (DerSimonian–Laird). Between-centre $I^2$ exceeded 70% for all three scores
> (SOFA 75.4%, OASIS 79.8%, SAPS-II 70.4%), with observed-to-expected (O/E) ratios spanning
> approximately 2.2-fold across centres (P10–P90: 0.69–1.54 for SOFA).
> **The drift is therefore a property of the setting rather than of any one score.**

### 中文对照

> **图3　三种急性严重度评分的跨中心校准截距漂移。** 每个面板为一种评分在 eICU-CRD 全队列
> （30,796 例、死亡 3,901 例）拟合的单预测因子 logistic 模型，再应用于 **103 家中心**（≥100 例且 ≥10 例死亡）。
> 各点为中心，按校准截距 $a_h$ 排序，**$a_h>0$ 表示实际死亡多于模型预测**；竖线为 95%CI（delta 法），
> 点大小 ∝ log(n)。三评分的院间 $I^2$ 均 >70%（SOFA 75.4%、OASIS 79.8%、SAPS-II 70.4%），
> O/E 比跨度约 2.2 倍。**说明漂移是"场景属性"，而非某一评分的缺陷。**

---

> **Sorting and colour.** Centres are sorted independently within each panel; the same x position does not denote the same centre across panels. Point colour simply re-encodes the calibration offset already shown on the y-axis and carries no additional information. Vertical bars are 95% confidence intervals for the offset by the delta method.

# Figure 2

### English legend

> **Discrimination transports across centres; calibration does not.**
> SOFA-based model, 103 eICU centres. Each point is a centre: x = its AUC (discrimination),
> y = its observed-to-expected ratio (calibration). The horizontal dashed line marks perfect
> calibration (O/E = 1); the dotted vertical line marks the pooled AUC (0.732). Marginal histograms
> show each marginal distribution. **Per-centre AUC ranged from 0.649 to 0.812 (a spread of 0.16),
> whereas per-centre O/E ranged from 0.69 to 1.54 (a 2.2-fold spread)** — calibration varies far more
> than discrimination. Point colour encodes $a_h$ (blue < 0, red > 0).

### 中文对照

> **图2　判别力跨中心可迁移，校准不可迁移。** 每点为一家中心：x = 该院 AUC，y = 该院 O/E 比。
> 水平虚线为完美校准（O/E=1），竖点线为合并 AUC（0.732）；边缘直方图为各边际分布。
> **逐院 AUC 跨度仅 0.16（0.649–0.812），而 O/E 跨度达 2.2 倍（0.69–1.54）**——校准的变异远大于判别力。

---
# Supplementary Fig. S1

### English legend

> **Supplementary Fig. S1. Measured case-mix barely reduces between-centre heterogeneity.**
> Successive adjustment of the SOFA-based model: M1 = SOFA alone; M2 = + age, sex;
> M3 = + comorbidity burden (Charlson) + invasive ventilation. Bars show between-centre $I^2$
> (random-effects meta-analysis, DerSimonian–Laird); numbers inside bars are the corresponding
> pooled AUCs. Adding age, sex, comorbidity burden and ventilation status raised the AUC by only
> **0.020** (0.732 → 0.752) while $I^2$ fell by just **5 percentage points** (75.4% → 70.1%).
> The red dashed line marks the conventional threshold for substantial heterogeneity ($I^2$ = 50%).
> **Note:** unmeasured case-mix (disease spectrum, referral patterns, socioeconomic status,
> pre-hospital course) cannot be excluded as a contributor. The remaining variation is therefore
> reported descriptively as **residual between-hospital variation** and is **NOT attributed to
> differences in quality of care**.

### 中文对照

> **图5　实测病例组合几乎不降低院间异质性。** 对 SOFA 模型逐级调整：M1=SOFA；M2=+年龄、性别；
> M3=+合并症负担(Charlson)+有创通气。加入年龄、性别、合并症与通气后 AUC 仅提高 **0.020**，
> $I^2$ 仅下降 **5 个百分点**。红虚线为 $I^2$=50% 的常用异质性阈值。
> **声明**：不能排除未测量病例组合（疾病谱、转诊模式、社会经济、入院前病程）的贡献；
> 因此剩余变异仅作**描述性**报告，**不归因于医疗质量差异**。

---

> **Reference bar.** The fourth bar refits the M1 model — the score alone — on exactly the patients and hospitals used by M3 (n = 27,236; 97 centres) and gives I² = 73.5%. Of the 5.2-percentage-point fall in I² from M1 to M3, 3.4 points are attributable to the change in analysis set and 1.9 points to the addition of the covariates. The reduction reflects the covariates rather than the change in analysis set.
>
> **Analysis set.** M1 and M2 use 30,796 patients and 103 hospitals; M3 and the reference bar use 27,236 patients and 97 hospitals, because Charlson comorbidity index is missing for 11.6% of eICU-CRD patients and M3 uses complete cases.
# Supplementary Fig. S2

### English legend

> **Supplementary Fig. S2. Position of a single-centre development cohort within the multicentre distribution.**
> The eICU-derived SOFA model (full-cohort coefficients) was applied to MIMIC-IV
> (8,579 patients, 1,654 deaths, 19.3%). MIMIC-IV is shown as the orange diamond; the grey points
> are the 103 eICU centres. MIMIC-IV had an AUC of 0.722 (0.732 within eICU), observed mortality
> 19.3% versus predicted 16.5% (O/E 1.17), and a calibration offset $a$ of +0.221 — **the 66th
> percentile of the eICU distribution**. The single-centre cohort is therefore not an outlier;
> the systematic miscalibration commonly observed when transporting a single-centre model
> reflects ordinary between-centre drift rather than an anomalous development cohort.

### 中文对照

> **图6　单中心开发队列在多中心分布中的位置。** 将 eICU 拟合的 SOFA 模型直接应用于 MIMIC-IV
> （8,579 例，死亡 1,654 例，19.3%）。MIMIC-IV 的 AUC 0.722（eICU 内 0.732），观测死亡 19.3% vs
> 预测 16.5%（O/E 1.17），校准截距 +0.221，**位于 eICU 103 家中心分布的第 66 百分位**。
> **单中心队列并不特殊**——迁移时常见的系统性失校准，反映的是普遍的中心间漂移。

---
# Figure 5

### English legend

> **(a)** Learning-curve analysis: for each $m$, $m$ patients per centre were drawn for local recalibration and the remainder for evaluation ($n\ge 2m$; 100 repeats per centre-$m$ cell). y axis: proportion of attempts with residual O/E within ±10% for S1 (intercept only) and S2 (intercept + slope); dotted line, no recalibration; dashed line, the 50% target; k, the number of contributing centres. **With 25 local patients, naive recalibration was worse than no recalibration at all (21.4% → 15.3%); the 50% target was never reached.**
>
> **(b)** Residual miscalibration |$a$| (median; band → P90).
>
> **(c)** Empirical-Bayes (EB) shrinkage removes the penalty: 103 centres; 200 paired resamples per centre-$m$ cell; $\bar a$ and per-centre SEs were leave-one-centre-out cross-fitted, so no centre's evaluation data entered its own shrinkage parameters. S0, no recalibration; S1/S2, naive; S3, EB shrinkage, $\hat a_{\mathrm{EB}}=\bar a+\lambda(\hat a_{\mathrm{ML}}-\bar a)$, $\lambda=\tau^2/(\tau^2+\mathrm{SE}^2)$. At $m$ = 25 the success rate rose from 15.5% to 24.3% (paired difference +9.05 percentage points, Wilcoxon P = 3.7×10⁻¹¹²), surpassing no recalibration (21.4%); median $\lambda$ 0.234/0.374/0.536/0.712 (m = 25/50/100/200), and residual |$a$| fell from 0.44 (naive) to 0.26.
>
> **(d)** Shrinkage parameters estimated once from eICU transfer to a different database: MIMIC-IV treated as a single new centre; $\bar a$ = +0.030 and $\tau^2$ = 0.131 fixed from eICU, never re-estimated; the offset to recover, $a^*$ = +0.221. EB shrinkage outperformed naive recalibration at every $m$ (at $m$ = 25: 47.0% vs 23.5%, +23.5 percentage points, Wilcoxon P = 6.3×10⁻⁷); **25 patients with shrinkage matched the success rate naive recalibration reached only with roughly 150 patients — a six-fold smaller local sample requirement.**
>
> **Notes.** The contributing-centre set shrinks with $m$; the S0 line is the *within-m* benchmark (not a learning effect). Panels a–b use 100 resampling attempts (15.3% at $m$ = 25), panels c–d 200 paired attempts (15.5%); both are correct independent draws — comparisons are within, not between, panels. MIMIC-IV is a single-centre database: panel d tests whether the shrinkage parameters transfer across databases and does not constitute multicentre external validation, which can only be evaluated within eICU itself (panel c). The dip at $m$ = 50 (panel d) is Monte-Carlo variation across the 200 attempts; read the trend across the panel.

### 中文对照

> **(a)** 学习曲线分析：每个 m 从每家中心抽取 m 例用于本地重校准、其余用于评估（n≥2m；每个 (中心, m) 组合重复 **100 次**）。y 轴为残余 O/E 落在 ±10% 内的比例（S1 仅校截距；S2 截距+斜率）；点线为不校准参照，虚线为 50% 目标；k 为参与中心数（横轴下方标注）。**25 例本地患者时，朴素重校准比完全不校准更糟（21.4%→15.3%）；50% 目标始终未达到。**
>
> **(b)** 残余失准 |a|（中位数；带 → P90）。
>
> **(c)** EB 收缩消除小样本惩罚：eICU 103 家中心；每 (中心, m) 组合 200 次配对重抽样；收缩目标 ā 与各中心 SE 由 **leave-one-centre-out** 交叉拟合估计，任何中心的评估数据都不进入其自身收缩参数。S0 不校准；S1/S2 朴素；S3 EB 收缩，â_EB=ā+λ(â_ML−ā)，λ=τ²/(τ²+SE²)。m=25 时达标率从 15.5% 升至 **24.3%**（配对差 **+9.05 个百分点**，Wilcoxon P=3.7×10⁻¹¹²），**超过不校准（21.4%）**；λ 中位数随 m 自适应（25/50/100/200 → 0.234/0.374/0.536/0.712），残余 |a| 从 0.44（朴素）降至 **0.26**。
>
> **(d)** 收缩参数仅在 eICU 估计一次、跨数据库迁移：把 MIMIC-IV 视为**一个新中心**；ā=+0.030、τ²=0.131 **固定自 eICU、绝不在 MIMIC 重估**；待恢复偏移 a*=+0.221。EB 收缩在每个 m 上均优于朴素（m=25：**47.0%** vs 23.5%，**+23.5 个百分点**，P=6.3×10⁻⁷）；**25 例 + 收缩 ≈ 150 例 + 朴素——本地数据需求缩小约 6 倍。**
>
> **说明**：(i) 参与中心集合随 m 收缩；S0 线是 m 内基准（不是学习效应）。(ii) 面板 a–b 用 100 次重抽样（m=25 为 15.3%），面板 c–d 用 200 次配对重抽样（15.5%）；两者都是正确的独立抽样——比较只在面板内进行。(iii) MIMIC-IV 为**单中心**库：面板 d 验证的是**收缩参数能否跨库迁移**，**不构成多中心外部验证**（后者只能在 eICU 内完成，见面板 c）。(iv) 面板 d 中 m=50 的轻微回落是 200 次重抽样的蒙特卡洛波动；趋势应跨整个面板阅读。
# Supplementary Fig. S3

### English legend

> **Supplementary Fig. S3. A centre's calibration offset is not a stable centre property.**
> eICU-CRD covers 2014–2015; **88 centres** contributed ≥50 patients and ≥5 deaths in each year.
> Each point is a centre: x = its calibration offset in 2014, y = its offset in 2015; colour =
> change ($\Delta a$ = 2015 − 2014). The dashed line is the identity line.
> The two years correlated at **Pearson $r$ = 0.586** ($r^2$ ≈ 34%; Spearman ρ = 0.563, P = 1.2×10⁻⁸);
> the median within-centre $|\Delta a|$ was **0.331** (P90 0.831). Variance decomposition attributed
> **41.6%** of the total between-centre variance to the within-centre temporal component.
> A centre's offset estimated in one year explains only about a third of its offset in the next —
> **any strategy relying on a one-off, fixed per-centre recalibration is inherently fragile**.

### 中文对照

> **图8　一家中心的校准偏移并不是稳定的中心属性。** eICU 仅覆盖 2014–2015；**88 家中心**两年各
> ≥50 例且 ≥5 例死亡。两年 a_h 的 Pearson **r = 0.586**（r²≈34%）；同一中心两年 |Δa| 中位 **0.331**；
> 方差分解显示**院间总方差中 41.6% 来自院内时间成分**。**依赖"一次性固定重校准"的策略本质上不稳固。**

---
# Figure 4

### English legend

> **(a)** Between-centre heterogeneity by centre size. Centres were split into tertiles by
> sample size; bars are $I^2$ and the orange line is the between-centre variance $\tau^2$.
> Heterogeneity **increased** with centre size (small: $I^2$ 56.7%, $\tau^2$ 0.093;
> medium: 69.8%, 0.117; large: 83.9%, 0.143). Had the apparent drift been driven by sampling
> noise, the least precisely estimated (small) centres would have shown the greatest heterogeneity;
> the opposite was observed, indicating that the between-centre variation is real.
>
> **(b)** Clinical impact of the same decision threshold in different centres. For each threshold
> $p_t$, points are the median and bars the P10–P90 range of the observed mortality among patients
> the model classified as high risk (112 centres with ≥100 patients); the red dashed line is the
> overall cohort mortality (12.7%). At $p_t$ = 0.20 the observed mortality among flagged patients
> ranged from **15% to 52% (3.5-fold)**. Model-guided escalation yielded **negative net benefit in
> 6.2%, 17.0%, 21.4% and 22.3% of centres** at $p_t$ = 0.10, 0.20, 0.30 and 0.40 respectively —
> i.e. in up to one in five centres the model performed worse than treating everyone.

### 中文对照

> **(a)** 按中心规模三分位分层的异质性。**异质性随中心规模增大而增强**（小：I² 56.7%、τ² 0.093；
> 中：69.8%、0.117；大：83.9%、0.143）。若表观漂移主要由抽样噪声造成，估计最不精确的小中心应异质性最高，
> **实测恰恰相反**——说明院间变异是真实存在的。
>
> **(b)** 同一决策阈值在不同中心的临床影响。在 p_t=0.20 时，被判高风险者的实际病死率从 **15% 到 52%（3.5 倍）**；
> **净获益为负**（模型指导的升级治疗比"全部收治"更差）的中心比例在四个阈值下分别为
> **6.2% / 17.0% / 21.4% / 22.3%**——即最多五分之一的中心。

---

> **Centres contributing at each threshold.** The number of hospitals contributing to each threshold varies, because a hospital contributes only when it flags at least ten patients. At the higher thresholds the flagged subgroup is small in many centres, so the observed mortality among flagged patients is imprecise and the 10th-to-90th percentile range widens accordingly.

---

# 统计方法句（可复用于各图注末尾）

- **异质性**：random-effects meta-analysis (DerSimonian–Laird); $I^2$ and $\tau^2$ reported.
  Three-stage sensitivity confirmed τ² estimates of 0.131 (DL), 0.126 (Paule–Mandel) and 0.130 (REML)
  (relative range 3.9%); a one-stage random-intercept multilevel logistic model gave a lower τ²
  (0.065), consistent with the fixed-slope two-stage estimator absorbing part of the
  between-centre slope variation (per-centre calibration slope P10–P90 = 0.72–1.64).
- **重抽样**：each (centre, $m$) combination repeated 100–200 times; paired comparisons by Wilcoxon signed-rank test.
- **收缩参数**：leave-one-centre-out cross-fitting to prevent information leakage from the evaluation set.
- **校准截距**：calibration-in-the-large offset $a_h$ solved numerically such that the mean recalibrated
  prediction equals the observed event rate; SE by the delta method.
