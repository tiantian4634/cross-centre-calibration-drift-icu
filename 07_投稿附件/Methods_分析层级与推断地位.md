# Methods —— 分析层级与推断地位（可直接插入正文）

对应任务②：明确区分**探索性/描述性**与**验证性（事前判据）**分析。
中英对照，英文为投稿版。

---

## 英文版（投稿用）

### Analysis framework and inferential status

Analyses were assigned to one of two inferential tiers, and the assignment is reported in the manuscript so
that readers can weight the findings accordingly. **This classification was fixed after the analyses were
completed and is disclosed as such; it is not a claim that all analyses were confirmatory.**

**Descriptive / exploratory tier.** The magnitude of between-centre variation in calibration, its
comparison across three severity scores, its relation to measured case-mix, its year-to-year stability
within a given centre, its relation to centre size, and its clinical consequences at fixed decision
thresholds were estimated without pre-specified hypothesis tests. These are reported as **estimates with
interval bounds**, not as tests of a hypothesis, and no claim of statistical significance is attached to
them.

**Confirmatory tier (pre-specified criterion).** Four analyses were each planned with an explicit criterion
*and* with an explicit instruction for the case in which that criterion was not met:

| Analysis | Pre-specified criterion | Criterion met? |
|---|---|---|
| E — local recalibration learning curve | Report the smallest local sample size *m* at which the success rate reaches 50%; if none is reached, state so | **No** — never reached within m = 200 |
| I — empirical-Bayes shrinkage vs naive | At m = 25 the shrinkage strategy must exceed naive recalibration; at m ≥ 100 it must not be worse by more than 5 percentage points | **Yes** |
| J — transfer of shrinkage parameters to a second database | At m = 25 shrinkage must exceed both naive recalibration and no recalibration | **Yes** |
| K — agreement of τ² across estimation frameworks | Relative range across the three two-stage estimators < 25%, and the one-stage multilevel estimate within 50% of their median | **Partly** — first clause met (3.9%), second clause **not** met (multilevel τ² 50.1% lower) |

**Two of the four pre-specified criteria were not met, and both are reported as negative findings.** They
are not reframed after the fact: analysis E is reported as showing that naive local recalibration has a
small-sample penalty that persists to 200 patients, and analysis K is reported as a genuine disagreement
between two-stage and one-stage estimators, together with a proposed mechanism and a sensitivity analysis
demonstrating that the principal conclusion is unaffected.

**Multiplicity.** Because the confirmatory analyses were four in number and were each defined by a
single pre-specified criterion evaluated once on the full cohort, no formal adjustment for multiple
comparisons was applied. The descriptive analyses involve no hypothesis testing. Readers should interpret
the interval bounds in the descriptive tier as measures of precision, not as tests.

**Software and reproducibility.** Analyses were performed in Python 3.14 with pandas, NumPy, scikit-learn,
scipy, statsmodels and DuckDB. The random seed was 20261019; resampling used explicitly seeded
`numpy.random.Generator` instances. Database access was **read-only** throughout. All analysis scripts are
available (see Code Availability); running them reproduces every number reported here. The analysis plans
for all analyses were written before execution and are reproduced in Supplementary Item S1, including a
disclosure of one file-timestamp defect and the two pre-specified criteria that were not met.

---

## 中文版（对照用）

### 分析框架与推断地位

所有分析被归入两个推断层级之一，并在正文中明示，以便读者据此权衡结论强度。
**该归类是在分析完成后确定的，据实披露；并非声称所有分析均为验证性分析。**

**描述性/探索性层级**：院间校准变异的大小、其在三种严重度评分间的比较、与实测病例组合的关系、
同一中心内的年际稳定性、与中心规模的关系，以及在固定决策阈值下的临床后果——这些均**未设事前假设检验**，
以**带区间界的估计值**报告，不附加任何"统计学显著"的主张。

**验证性层级（事前判据）**：四项分析各自写明了明确的判据，**并同时写明判据不成立时如何处理**：

| 分析 | 事前判据 | 判据是否成立 |
|---|---|---|
| E 本地重校准学习曲线 | 报告达标率首次达到 50% 的最小本地样本量 m；若始终未达到，如实写明 | **否** —— m ≤ 200 始终未达到 |
| I EB 收缩 vs 朴素 | m=25 时收缩须优于朴素；m≥100 时不得差 5 个百分点以上 | **是** |
| J 收缩参数跨库迁移 | m=25 时收缩须同时优于朴素重校准与完全不校准 | **是** |
| K τ² 估计框架一致性 | 两阶段三估计量相对极差 <25%，且多水平估计与其中位数相差 <50% | **部分成立** —— 第一条满足（3.9%），第二条**不成立**（低 50.1%） |

**四项事前判据中有两项不成立，二者均作为阴性结果如实报告**，未做事后重构：
E 报告为"朴素重校准的小样本惩罚持续至 200 例"；K 报告为两阶段与一阶段估计量之间的真实分歧，
并给出可能机制与敏感性分析，证明主结论不受影响。

**多重性**：验证性分析共四项，每项均由单一事前判据在全队列上评估一次，未作多重比较校正；
描述性分析不涉及假设检验。描述性层级的区间界应理解为**精度度量**，而非检验。

**软件与可重复性**：Python 3.14 + pandas / NumPy / scikit-learn / scipy / statsmodels / DuckDB；
随机种子 20261019，重抽样均使用显式播种的 `numpy.random.Generator`。数据库全程**只读**。
所有脚本已公开（见代码可得性声明），运行即可复现本文全部数字。各分析计划均写于执行之前，
见补充材料 S1，其中含一处文件时间戳缺陷的披露，以及两项未成立的事前判据。
