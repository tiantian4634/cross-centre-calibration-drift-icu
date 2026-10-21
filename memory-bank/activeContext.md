# Active Context — 路B 跨中心校准漂移论文（Sci Rep 投稿准备）

> 最后检查点：2026-10-21（第 2 轮）｜ 会话：占位符清零 + 伦理声明成稿

## 🎯 当前焦点
占位符全部清零，稿件可直投；剩余仅「投稿前统一 push → 上传 Sci Rep 系统」两步。

## 📝 本轮会话进展（2026-10-21 第 2 轮）
1. **作者名单定稿（2 人，不再有第二作者）**：`Junzhi Chu¹, Tiantian Zhang²*`
   - ¹ = First Clinical Medical College, Zhejiang Chinese Medical University（一临床医学院）
   - 通讯邮箱 `tiantian4634@163.com`；ORTID `0009-0000-2350-8008`（与 CITATION.cff 一致）
   - 注意：第一作者名 Chu Junzhi=Junzhi Chu，勿写成 Junzi/Chu Junzhi
2. **伦理声明成稿（关键决策，见 decisionLog 决策 7）**：不写本地委员会/免审文号，采用 PhysioNet
   公开库领域惯例（Liu 2024 Sci Rep「CITI record number」/ Zhang 2023 Sci Rep / Hu 2025 BMC MIDM /
   Yamamoto 2026 medRxiv 四例实文核对）：上游 IRB（MAT+BMDC）批准 + HIPAA Safe Harbor 全去标识
   → 免本地伦理审批、免知情同意、含赫尔辛基声明。培训记录号 68897765（T.T.Z.）写入。
   医院口径（数据库文章免伦理审批）与领域惯例完全一致。
3. **CRediT 简写定稿**：Zhang = conceived/designed, data extraction, analyses, code, figures,
   original draft, supervision; Chu = study design, clinical interpretation, drafting/revision;
   Both authors approved + accountable。Competing interests = "The author(s) declare no competing interests."
4. **审稿人 5 人维持不动**（用户确认，无删改）。
5. **检查器两处探针修正**：
   - `回归检查_SciRep合规.py`：IDENT 豁免集加 `68897765`（标识符不加千分位，Liu 2024 同例）
   - `质检_投稿包.py`：Author contributions 存活探针由 `CRediT` 改为 "Both authors approved the final version of the manuscript"
6. **全链路重跑全部绿**：装配 76.7KB/1003 行 32 文献；Methods 数字全对；Results 95 项 ✔；
   词数 4438/4500；千分位 ✔；图注硬编码无异常；旧数值 0；STROBE 引文 54/54；装配质检 12 段顺序全 ✔；
   补充材料 0.68MB/11 页；投稿包重建完成，**包内占位符清单 = 0 处**。
7. **变更文件**：装配_Manuscript.py、08_正文/{Methods,TitlePage,BackMatter,Manuscript}.md、
   07_投稿附件/SciRep_投稿合规清单.md、两个检查脚本、Supplementary_Information.pdf；投稿包全量再生。

## ✅ 润色三轮定稿（2026-10-21 第二批）
- **已批准并执行**：§ 标记 ×2 清理；in order to→to；TRIPOD/STROBE/RECORD 首现全称展开（Methods 数据可用性前 Reporting guidelines 节）；
  SE 首现定义（centre-level 与 (SE)）；破折号 50→21：5 对转括号/冒号清单（M1/M2/M3 塔、M1 提示语、whose offsets、m 学习曲线、τ² 三值），
  13 处单破折号转分号/冒号/逗号；保留论文命题句 2 对（Intro 开头 Calibration—whether…、Discussion That missing quantity—…）+ Methods 「hospital—the level…」对；
  最长 2 条真实散文长句拆分（111 词 cut-points 枚举句、77 词 punished-estimator 验证句；其余 >70 词均为分句器把关键词行/粗体句首误并的假象）。
- **保真校验**：对 git HEAD 全文逐 token diff——数字/引用序列完全一致（仅 S1 (§S1.6)→S1.6 引起的计数假象）；改动全部为已批准标点样式级。
- **全链路重跑全绿**：装配 76.9KB/1007 行；词数 4436/4500（余 64）；摘要 200/200；Methods 数字 ✔；Results 95 项 ✔；
  红线 ✔；引用 32/32 ✔；装配质检 ✔；投稿包重建（DOCX/PDF 22 页/STROBE 清单/审稿人名单）；Markdown 残留 0；占位符 0。
- **发布前安全核查**：CSV 无患者级 ID/时间列 ✔；凭据实质命中 0 ✔；脚本硬编码本地盘符 = 已知误报。
- **推送前最终核查标 ✘ 的唯一原因**：shrinkage_raw.csv / learning_curve_raw.csv 历史已入库（脚本自注「在库(可接受)」，
  内容级扫描证明无 ID/时间列，纯重抽样聚合计数）——推送与否留给用户决定。

## ⚠️ 待解决（等用户）
- [x] ~~投稿前统一 git push~~ **✅ 已推送**（7aca874 → origin/main，2026-10-21，授权完成）
- [ ] STROBE checklist 页码（投稿系统要求 n/a 就填 n/a）
- [ ] Cover letter 最终过目（审稿人段已备好英文粘贴段）

## 🔜 下一步
1. ~~push~~（done）→ 上传 Sci Rep 系统（suggested reviewers 用名单 5 人；excluded 可不填）
2. 投稿系统录入时：标题/作者/单位/摘要与标题页源**逐字比对**；ORCID 0009-0000-2350-8008 填入系统
3. 远期：300 例下篇论文立项（data dictionary 先行）
4. 伏笔：审稿人若要求时域稳定性主图化 → S3 小节后移 §J 后 + 升 Fig.6 免重排路径；伦理若被编辑追问
   → 再补院级「免于伦理审查」认定函（修回阶段可补，不阻塞投稿）
