# Scientific Reports 投稿合规清单

**来源（两份，均为官方原文，本地已留档可离线核对）**
1. **Submission guidelines**：<https://www.nature.com/srep/author-instructions/submission-guidelines>
   （本地留档：`官方_SciRep_submission_guidelines.txt`，366 行）
2. **Checklist for initial submissions（必填清单 PDF）**：<https://www.nature.com/documents/srep-checklist-for-initial-submissions.pdf>
   （本地留档：`官方_SciRep_checklist.txt` + `官方_SciRep_checklist.pdf`，3 页）

> ⚠️ **Submission guidelines 第 70 行明说**："For a definitive list of **which limits are mandatory**
> please visit the submission checklist page." —— **必填项在清单里，不在指南正文。**
> 两份都已取回。清单原文：*"manuscripts that do not comply may be returned for changes before they
> are assigned to an EBM."* **不合规会被退回，不进入评审。*

生成：2026-10-20　｜　自动核对脚本：`回归检查_SciRep合规.py`（可重复运行）

---

## 一、核对状态总览

| 分组 | 自动核对结果 |
|---|---|
| 摘要（≤200 词 / 非结构化 / 无引用） | ✅ **199 词**，无小标题，无引用 |
| 标题（≤20 词 / 单句 / 无双关） | ✅ 14 词（候选 A/B 均 14 词） |
| 关键词（≤6） | ✅ **6 个**（Intensive care · Calibration · Severity score · External validation · Data drift · Empirical Bayes） |
| **图注（每条 ≤350 词）** | ✅ **10/10 全部达标**，最长图1 = 293 词 |
| Methods 六项必备段落 | ✅ LLM 声明 / 伦理（占位）/ STROBE / Software / 分析层级 / 统计报告 |
| 千分位分隔（≥5 位须加逗号） | ✅ 通过（报出的 `20261019` 是随机种子常量，非数量，本就不应加逗号） |
| **Display items ≤ 8** | ❌ **现有 10 图 + 3 表 = 13**，须砍到 8 |
| 稿件结构必备段落 | ⬜ 7 项待 Results/Intro 完成后定稿 |

---

## 二、🔴 我之前没抓到的硬性要求（新增）

| # | 官方原文要点 | 对我们意味着 |
|---|---|---|
| 1 | **Manuscript File: "Only one file permitted"**（.doc/.docx/.tex/.pdf） | 正文+图+表**必须合成一个文件**（首次投稿允许内嵌图，≤3 MB） |
| 2 | **Main Tables: "Do not upload separately — Must be included in the Manuscript File"**，且**不能是嵌入的图片**，须可编辑格式 | 表必须在 .docx 里做成真表格，**不能截图** |
| 3 | **"Tracked changes must not be used"** | 修订痕迹不得保留；要标改动用**高亮工具或改字色**，**不得用斜体**标改动 |
| 4 | **Author contributions 放在 references 之后**，且**每位作者**都要列出 | 结构顺序：…References → Author contributions → Data Availability |
| 5 | **图注也放在 references 之后**；**补充材料的图注不得放进正文**，须放在补充文件内 | 与我们"图注集中一文档"的现状一致，但**装配时须移到 References 之后** |
| 6 | **Data Availability 标题须恰为 `'Data Availability'`**，位置在**正文末、References 之前** | 现有材料在 `Data_Code_Availability.md`，须转成独立小节并**精确用这个标题** |
| 7 | **Competing interests 须置于标题 `"Additional Information"` 下**，且**与投稿系统中填的一致**，须披露**财务与非财务**利益 | 需写且逐位作者声明 |
| 8 | **Schemes、graphical abstracts、boxes 一律不许**；不收 Cover 图 / 目录图 | 我们不用这些 ✅（但要确认没有把流程图做成 box 风格） |
| 9 | **Abstract 不得含引用**；**标题与摘要须与投稿系统中所填完全一致** | ✅ 摘要无引用；**录入系统时逐字复制** |
| 10 | **单位须含国家**，且用**上标数字**把作者与单位对应 | 标题页要写成 `张¹²` + `1 浙江中医药大学，杭州，中国` 形式 |
| 11 | **通讯作者用 `*` 标注，标题页须有邮箱** | |
| 12 | **伦理声明须确认 "informed consent was obtained from all participants"** | ⚠️ 我们是**公开去标识数据二次分析**，通常属"免除知情同意"——**须明确写出是豁免/不适用**，不能含糊 |
| 13 | **Table 不得超过一页** | 表1–表3 需核长度 |
| 14 | **图表编号须按出现顺序**；多面板图**各面板须逻辑关联** | 我们 6 张多面板图需能说明关联（如图10 左=残余偏移、右=达标率，同一实验两种指标） |

---

## 三、图件格式要求（官方）

| 项 | 要求 | 我们现状 |
|---|---|---|
| 允许格式 | `.jpg .eps .tiff .psd .png .pdf` | ✅ 有 **PNG 600dpi + PDF** |
| 分辨率 | **300 DPI**（终稿） | ✅ 600 dpi |
| 线条图 | 官方建议**矢量（EPS 或 AI）** | ✅ PDF 是矢量；PNG 600dpi 作为位图版本 |
| 字体 | **clear sans-serif**（如 Helvetica） | ✅ DejaVu Sans（无衬线） |
| **字例大小写** | **"Lettering in figures should be in lower-case type, with only the first letter of each label capitalised"** | ⬜ **需逐图检查**：标签须为句首大写，其余小写 |
| 图内分面板标记 | 小写粗体 **a, b, c** | ⬜ 需检查 |
| 误差棒 | 图注须写明**误差的统计处理** | ✅ 图10 注明 "median; band → P90"；**其余图待逐条确认** |
| 纵轴 | **"Never truncate the vertical axis of histograms"** | ⬜ 需检查 |
| 数字格式 | ≥5 位数用千分位逗号 | ✅ 通过 |
| 表格 | 可编辑、**不支持彩色表格** | ⬜ 需检查现有表（若有配色须改黑白） |

---

## 四、第一单位冲突 —— ✅ 已解决（2026-10-20）

**Submission guidelines 第 187 行**：

> *"The primary affiliation for each author should be the institution where **the majority of their
> work was done**."*

**与学位约束「第一单位＝浙江中医药大学」的潜在冲突，已由作者确认如下安排，属可自圆其说的写法：**

| 角色 | 作者 | 第一单位 |
|---|---|---|
| 第一作者 | **Junzhi Chu** | **First Clinical Medical College, Zhejiang Chinese Medical University**（本研究作为学位课题在此完成主要工作） |
| 通讯作者 `*` | Tiantian Zhang | Xianju People's Hospital, Zhejiang Southeast Campus of Zhejiang Provincial People's Hospital, Affiliated Xianju's Hospital, Hangzhou Medical College, Xianju, Taizhou, Zhejiang, China |

**理由（如需向编辑说明）**：第一作者以该研究为学位课题、在浙江中医药大学完成主要工作；
通讯作者的实际工作单位为仙居县人民医院。两单位均为真实隶属，**用上标编号分别列出**，
不互相遮蔽。

**仍需确认**：浙中医大所在城市的正式英文写法（Hangzhou）；是否还有其他共同作者及其单位。

---

## 五、投稿前必须完成的清单（🔴 = 阻塞）

### 🔴 阻塞项
- [ ] **砍图到 display items ≤ 8**（现 10 图 + 3 表 = 13）——方案见 `项目归档总结_交接文档.md` §9
- [ ] **正文写完**（Introduction / Results / Discussion），正文 ≤ 4,500 词（不含摘要、Methods、参考文献、图注）
- [ ] **伦理声明**填入真实委员会名称 + 批件号，并**明确写出知情同意为豁免/不适用**（清单第 12 条）
- [ ] **第一单位决定**（见 §四）

### 📄 稿件结构（官方规定的顺序）
- [ ] 标题页：作者 + 上标单位（**含国家**）+ 通讯作者 `*` + 邮箱
- [ ] 摘要（≤200 词、非结构化、无引用）
- [ ] 关键词（≤6）
- [ ] Introduction
- [ ] **Results（带小标题）**
- [ ] Discussion（**不带小标题**）
- [ ] Methods
- [ ] **References**（编号列表，文内方括号，Nature 格式，≤60 条）
- [ ] **Author contributions**（References 之后，逐位作者）
- [ ] **Data Availability**（标题须精确，References **之前**，正文末）
- [ ] **Additional Information**（Competing interests，逐位作者，与系统一致）
- [ ] **图注**（References 之后，每条 ≤350 词）
- [ ] 表格（正文内、可编辑、≤1 页、无彩色）

### 📎 随稿上传
- [ ] Cover letter（.doc/.docx/.pdf；**含通讯作者单位联系方式、说明为何适合 Sci Rep、推荐与回避审稿人、是否曾与 EBM 接洽**）
- [ ] **Manuscript File 单一文件**（首次投稿可内嵌图，≤3 MB）
- [ ] 主图单独文件（PNG/PDF 均可，600 dpi）
- [ ] **Supplementary Information 单独一个文件**（优先 PDF，≤50 MB）
- [ ] 补充数据集若为数据表 → **单独 .xlsx**
- [ ] 无 tracked changes；如需标改动用**高亮或字色**（不得用斜体）
- [ ] **标题与摘要与投稿系统中所填逐字一致**

### ✅ 已完成
- [x] 摘要 199 词、非结构化、无引用
- [x] 标题 14 词、单句、无双关
- [x] 关键词 6 个
- [x] 图注 10 条全部 ≤350 词
- [x] Methods 六项必备段落齐备（LLM / 伦理占位 / STROBE / Software / 分析层级 / 统计规则）
- [x] Data & code availability 材料已备（含 Zenodo DOI），待转成独立小节
- [x] 预注册补充材料 S1 已备（含 §S1.6 更正披露、§S1.7 空缺披露）

---

## 六、复核方式

```powershell
cd "E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
python -X utf8 "回归检查_SciRep合规.py"     # 摘要/标题/图注/结构/display items
python -X utf8 "回归检查_文档旧数值.py"       # 过期数字
python -X utf8 "回归检查_图注硬编码.py"       # 图上写死的数字
```

**每次改动正文或图后都应重跑，并显式看退出码**（本项目记录过一次静默失败的教训）。