# Scientific Reports 投稿版摘要

**目标期刊规范**：摘要 ≤200 词 · 非结构化（无小标题）· 不含参考文献与图 · 关键词 ≤6 个

---

## 摘要（英文投稿版）

Acute severity scores are often assumed to transport between hospitals. In 30,796 patients aged
≥65 years from 187 intensive-care units we examined whether such scores discriminate and calibrate
alike across centres. Discrimination was moderate and nearly constant (pooled AUC 0.732 for SOFA;
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
and transferring to a second database without refitting. Discrimination transports; calibration
does not.

---

## 规范核对表

| 要求 | 状态 |
|---|---|
| ≤200 词 | 见文末自动校验 |
| 非结构化（无小标题） | ✅ |
| 不含参考文献与图 | ✅ |
| 关键词 ≤6 | ✅ 用下方 6 个 |
| 标题 ≤20 词、单句 | ✅ 见候选标题 |

---

## 关键词（6 个，达上限）

Intensive care · Calibration · Severity score · External validation · Data drift · Empirical Bayes

> 原 BMC 版写了 11 个关键词（含 SOFA/OASIS/SAPS-II/eICU/MIMIC-IV）。
> **必须砍到 6 个**。数据库与具体评分名在正文中被检索到即可，不必占用关键词位。

---

## 标题候选（均 ≤20 词、单句、无双关）

Sci Rep 要求标题「用一句科学准确的句子描述文章主旨」。

**推荐：**
> Discrimination transports, calibration does not: calibration drift in severity scoring across 187 intensive-care units

（17 词，删掉了后半段「sample size needed to recalibrate」以压进 20 词内，同时保留核心反差）

**备选 A（更突出方法学贡献）：**
> Between-centre calibration drift in severity scoring and the local sample size needed to recalibrate

（16 词，无反差句式，更保守）

**备选 B（最贴 Sci Rep「一句话主旨」）：**
> Discrimination travels but calibration does not, and naive local recalibration makes it worse

（15 词，把两个发现都放进标题，但「worse」可能显得结论化）

---

## 压缩时丢弃的内容（记录在案）

从 BMC 版 410 词压到 200 词时，以下内容被移出摘要——**全部保留在正文，不可丢**：

| 丢弃内容 | 去处 |
|---|---|
| 三评分各自的 I² 与合并 AUC | Results 正文 + Table 1 |
| 病例组合阶梯的具体数字（AUC +0.020、I² −5 pp） | Results 正文 |
| 规模分层的 τ² 0.093→0.143 | Results 正文 |
| 41.6% 时间成分占比 | Results 正文 |
| 收缩权重 λ=0.234 自适应 | Results 正文 |
| MIMIC 转移的具体数字（47.0% vs 23.5%、+23.5 pp、约 6 倍） | Results 正文 |
| τ² 框架分歧（3.9% / 低 50%） | Results 正文 + 局限性 |
| 「本项为统计学建议，非临床推荐」 | **Discussion 必须保留**（三条措辞红线之一） |
| 「两项判据未成立」 | 保留为「a threshold never reached」；完整表述见 Results 与补充材料 S1 |

---

## 三条措辞红线（压缩后仍全部守住）

1. 漂移仅称 **drift / variation**，全文未出现「医疗质量差异」
2. MIMIC 写作 **a second database**，**未称**「外部多中心验证」
3. 「非临床推荐」一句已移至 Discussion——**压缩时绝不可整段删除**