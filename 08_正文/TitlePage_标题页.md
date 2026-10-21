# 标题页（Title Page）—— Scientific Reports 投稿版

> **Sci Rep / 官方清单对标题页的要求**
> - 标题须与投稿系统所填**逐字一致**
> - 作者姓名用**上标数字**与单位对应
> - 单位须**含国家**，且按数值顺序排列（1,2，不能 2,1）
> - **通讯作者用 `*` 标注，标题页须给出其邮箱**
> - 标题 ≤20 词、单句、无双关/习语
> - **不得使用脚注**
>
> **占位符**：`⟨…⟩` 为待填项。填完后删除所有提示文字。

---

## 标题

**Discrimination transports, calibration does not: calibration drift in severity scoring across
187 intensive-care units**

<!-- 14 词 ✔ ≤20；单句 ✔ 无双关 ✔
     备选 A（更保守，突出方法学）：
     "Between-centre calibration drift in severity scoring and the local sample size needed to
      recalibrate"
     备选 B（最贴 Sci Rep「一句话主旨」）：
     "Discrimination travels but calibration does not, and naive local recalibration makes it worse" -->

---

## 作者与单位

**Junzhi Chu¹, Tiantian Zhang²\***

¹ First Clinical Medical College, Zhejiang Chinese Medical University, Hangzhou, Zhejiang, China
² Xianju People's Hospital, Zhejiang Southeast Campus of Zhejiang Provincial People's Hospital,
Affiliated Xianju's Hospital, Hangzhou Medical College, Xianju, Taizhou, Zhejiang, China

\* Corresponding author. Email: tiantian4634@163.com

---

### 生成 Word 正文时的排版提示（不进稿）

单位须**按编号顺序**列出（1,2），不能先写 ² 再写 ¹。
同一单位的多个官方称谓（如 ² 中仙居县人民医院 / 浙江省人民医院浙东南院区 /
杭州医学院附属仙居医院）**合并为一条**，不要拆成多个编号——它们是同一所医院。

上标格式（Word 中）：`Zhang T¹, ⟨Name⟩²` + 单位行前加上标 1/2。
通讯作者星号置于其姓名上标数字之后：`Zhang T²*`。

---

## 作者与单位的完整信息表（供投稿系统录入）

投稿系统中填的内容须与稿内**完全一致**（Sci Rep 清单原文：*"All author (corresponding and
contributing) details are included on the submission system as well as in the Manuscript File"*）。

| # | 姓名 | 顺序 | 单位编号 | 单位 | 邮箱 | 通讯作者 |
|---|---|---|---|---|---|---|
| 1 | Junzhi Chu | 第一作者 | ¹ | First Clinical Medical College, Zhejiang Chinese Medical University, Hangzhou, Zhejiang, China | | |
| 2 | Tiantian Zhang | 通讯作者 | ² | Xianju People's Hospital, … Hangzhou Medical College, Xianju, Taizhou, Zhejiang, China | tiantian4634@163.com | ✅ `*` |

**ORCID**：Tiantian Zhang = `https://orcid.org/0009-0000-2350-8008`（已入库 CITATION.cff；投稿系统中须填写）

---

## 待填清单（🔴 = 投稿阻塞）

- [x] 🔴 同事姓名（第一作者）—— Junzhi Chu（浙江中医药大学第一临床医学院）
- [x] 🔴 通讯作者邮箱 —— tiantian4634@163.com
- [x] 🔴 是否还有其他共同作者 —— 无，两名作者定稿（2026-10-21）
- [x] 浙中医大城市写法确认（Hangzhou）
- [ ] 通讯作者 ORCID 是否填入投稿系统（`0009-0000-2350-8008`，系统填写时用）
- [ ] 标题、作者、单位、摘要录入投稿系统后与本文件**逐字比对**

---

## 与其他文件的同步要求

| 改了这里 | 还要同步 |
|---|---|
| 标题 | `CITATION.cff` 的 `repository-code` 无关；**摘要文件的标题候选段**、`README.md` 若含标题 |
| 作者/单位 | 投稿系统、`CITATION.cff`（仅代码署名，勿混淆）、Author contributions、Competing interests |
| 邮箱 | 投稿系统、稿内标题页两处 |