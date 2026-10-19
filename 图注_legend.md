# 跨中心校准漂移研究 · 图注（Legends）合集

生成：2026-10-19（B）
用途：SCI 投稿用**英文图注（正文/投稿系统用）** + 中文对照（自己与导师核对用）。

---

## ⚠️ 版式约定（务必遵守）

图内**不出现**主标题、解释性副标题、底部文字注释——这些信息**全部写在本文件的图注里**。
图内只保留：面板标识、坐标轴标签、图例、图内统计标注框。

**被从图上删掉、但必须保留在图注里的关键声明**（尤其图5、图9）：
> 「实测病例组合解释不了漂移」「残余院间变异不作医疗质量归因」——
> 这是**方法学红线**，删掉图注就等于丢了这条声明，审稿人会追问。

> **编号说明**：以下按**当前文件名**编号（图3–图11）。
> 正式投稿前若加流程图（图1）或调整顺序，需统一重编号；本文件的图注文字不受影响，只改编号即可。

---

# 图1　两库患者筛选流程图

### English legend

> **Figure 1. Flow of participants from eICU-CRD and MIMIC-IV into the analysis.**
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

# 图3　三评分的跨中心校准漂移

### English legend

> **Figure 3. Between-centre drift in calibration intercept for three acute-severity scores.**
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

# 图4　判别力可迁移，校准不可迁移

### English legend

> **Figure 4. Discrimination transports across centres; calibration does not.**
> SOFA-based model, 103 eICU centres. Each point is a centre: x = its AUC (discrimination),
> y = its observed-to-expected ratio (calibration). The horizontal dashed line marks perfect
> calibration (O/E = 1); the dotted vertical line marks the pooled AUC (0.732). Marginal histograms
> show each marginal distribution. **Per-centre AUC ranged from 0.649 to 0.812 (a spread of 0.16),
> whereas per-centre O/E ranged from 0.69 to 1.54 (a 2.2-fold spread)** — calibration varies far more
> than discrimination. Point colour encodes $a_h$ (blue < 0, red > 0).

### 中文对照

> **图4　判别力跨中心可迁移，校准不可迁移。** 每点为一家中心：x = 该院 AUC，y = 该院 O/E 比。
> 水平虚线为完美校准（O/E=1），竖点线为合并 AUC（0.732）；边缘直方图为各边际分布。
> **逐院 AUC 跨度仅 0.16（0.649–0.812），而 O/E 跨度达 2.2 倍（0.69–1.54）**——校准的变异远大于判别力。

---

# 图5　实测病例组合几乎解释不了漂移

### English legend

> **Figure 5. Measured case-mix barely reduces between-centre heterogeneity.**
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

# 图6　单中心开发队列在多中心分布中的位置

### English legend

> **Figure 6. Position of a single-centre development cohort within the multicentre distribution.**
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

# 图7　本地重校准学习曲线（朴素方法）

### English legend

> **Figure 7. How many local patients does a centre need to recalibrate an externally developed model?**
> SOFA-based model, eICU centres with ≥200 patients; for each $m$ the calibration set and the
> evaluation set were required to be at least equal in size ($n \ge 2m$), and each (centre, $m$)
> combination was repeated **100 times**. Two strategies were compared: recalibrating the
> intercept only (S1) and recalibrating both intercept and calibration slope (S2).
> Left: residual miscalibration $|a|$ (median across centres; band → P90).
> Right: the proportion of resampling attempts whose residual O/E fell within ±10%.
> **With 25 local patients, naive recalibration was worse than no recalibration at all**
> (residual $|a|$ 0.31 → 0.45; ±10% success 21.4% → 15.3%), and even 200 patients succeeded in
> only 34% of attempts. Two-parameter recalibration was no better than intercept-only and was
> worse at small $m$. **Sample-size requirements for local recalibration are commonly underestimated.**

### 中文对照

> **图7　本地重校准需要多少例？** SOFA 模型，eICU 中 n≥200 的中心；每个 m 要求校准集与评估集
> 至少等大（n≥2m），每个 (中心, m) 组合重复 **100 次**。比较两种策略：仅校截距（S1）、
> 截距+校准斜率（S2）。**用 25 例本地数据做朴素重校准，比完全不校准更糟**（残余|a| 0.31→0.45；
> ±10% 达标 21.4%→15.3%），即使 200 例也只有 34% 成功。**本地重校准的样本量需求常被严重低估。**

---

# 图8　同一中心两年的校准偏移并不稳定

### English legend

> **Figure 8. A centre's calibration offset is not a stable centre property.**
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

# 图9　规模分层 与 临床影响

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

# 图10　分层收缩把小样本负收益翻盘为净收益

### English legend

> **Figure 10. Hierarchical shrinkage removes the small-sample penalty of local recalibration.**
> 103 eICU centres; **200 resamples** per (centre, $m$). The shrinkage target $\bar a$ and the
> between-centre variance $\tau^2$ were estimated by **leave-one-centre-out** cross-fitting, so no
> centre's evaluation data entered its own shrinkage parameters. Four strategies:
> S0 no recalibration; S1 naive intercept-only; S2 naive intercept + slope;
> **S3 empirical-Bayes shrinkage**, $\hat a_{\mathrm{EB}} = \bar a + \lambda(\hat a_{\mathrm{ML}} - \bar a)$
> with $\lambda = \tau^2/(\tau^2 + \mathrm{SE}^2)$.
> Left: residual miscalibration $|a|$ (median; band → P90). Right: proportion of resampling
> attempts landing within ±10% of perfect O/E. **Shrinkage reversed the small-sample penalty**:
> at $m$ = 25 residual $|a|$ fell from 0.45 (naive) to 0.26 and the ±10% success rate rose from
> 15.5% to **23.4%** (paired difference **+8.2 percentage points**, 19,678 pairs, Wilcoxon P = 2.5×10⁻⁹²)
> — surpassing even no recalibration (21.4%). The shrinkage weight adapted to sample size
> (median λ = 0.234, 0.374, 0.536 and 0.712 at $m$ = 25, 50, 100 and 200).

### 中文对照

> **图10　分层收缩消除本地重校准的小样本惩罚。** 103 家中心，每 (中心, m) 重复 **200 次**；
> 收缩目标 ā 与 τ² 由 **leave-one-centre-out** 交叉拟合估计，无任何中心的评估数据进入其自身收缩参数。
> **收缩把小样本惩罚翻盘**：m=25 时残余 |a| 从 0.45（朴素）降至 0.26，±10% 达标率从 15.5% 升至 **23.4%**
> （配对差 **+8.2 个百分点**，19,678 对，Wilcoxon P=2.5×10⁻⁹²），**已超过完全不校准（21.4%）**。
> 收缩强度随样本量自适应（m=25/50/100/200 时 λ 中位 = 0.234/0.374/0.536/0.712）。

---

# 图11　收缩参数可跨数据库迁移

### English legend

> **Figure 11. Shrinkage parameters estimated once from eICU generalise to a different database.**
> Outcome: proportion of resampling attempts with residual |O/E − 1| ≤ 10%; 200 resamples per $m$.
> **Left, internal validation:** 103 eICU centres, leave-one-centre-out (as Figure 10).
> **Right, external validation:** MIMIC-IV treated as a single new centre (8,579 patients, 1,654 deaths);
> the shrinkage target $\bar a$ = +0.068 and $\tau^2$ = 0.131 were **fixed from eICU and never
> re-estimated on MIMIC-IV**. The true offset to recover was $a^*$ = +0.221 (observed 19.3% vs
> predicted 16.5%, O/E 1.17). Empirical-Bayes shrinkage outperformed naive recalibration at every
> $m$ (at $m$ = 25: 53.5% vs 23.5%, paired difference **+30.0 percentage points**, Wilcoxon
> P = 7.4×10⁻¹³) and, critically, **25 local patients with shrinkage performed comparably to 200
> local patients without** (53.5% vs 53.0%) — an approximately **eight-fold reduction** in the
> local sample requirement.
>
> **Note:** MIMIC-IV is a **single-centre** database. This analysis tests whether the *shrinkage
> parameters* transfer across databases; it does **not** constitute multicentre external validation
> of the strategy, which can only be evaluated within eICU itself (Figure 10). The two must not be
> conflated.

### 中文对照

> **图11　收缩参数可跨数据库迁移。** 左：eICU 103 家中心 LOO（同图10）。右：把 MIMIC-IV 的 8,579 例
> 整体视为**一个新中心**，收缩目标 ā=+0.068、τ²=0.131 **完全固定自 eICU、绝不在 MIMIC 上重估**；
> 待恢复真值 a*=+0.221。EB 收缩在每个 m 上均优于朴素（m=25：53.5% vs 23.5%，配对差 **+30.0 个百分点**，
> P=7.4×10⁻¹³）；**25 例 + 收缩 ≈ 200 例 + 朴素**（53.5% vs 53.0%），本地数据需求降低约 **8 倍**。
>
> **声明**：MIMIC-IV 为**单中心**库。本分析验证的是"**收缩参数能否跨库迁移**"，
> **不是**该策略的多中心外部验证（后者只能在 eICU 内完成，见图10）。两者**不得混称**。

---

# 待补图（投稿前需完成）

| 编号（暂定） | 内容 | 状态 |
|---|---|---|
| **图1** | 两库患者筛选流程图（CONSORT 式） | ⬜ **未做**，须补 |
| 附图S1 | 逐院校准漂移 caterpillar（探测轮图1，n≥50 版） | ⬜ 候选，可并入主图或作附图 |
| 附图S2 | 病例组合 vs 残余漂移散点（探测轮图2） | ⬜ 候选 |

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
