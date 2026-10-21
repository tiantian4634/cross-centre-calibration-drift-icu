# Active Context — 路B 跨中心校准漂移论文（Sci Rep 投稿准备）

> 最后检查点：2026-10-21 ｜ 会话：投稿收尾+审稿人+撞题引用调研

## 🎯 当前焦点
论文本体已定稿全绿，处于「等用户填占位符 → 投稿前统一 push → 上传投稿系统」阶段；本轮补完了审稿人名单、撞题预印本引用、同题期刊落点调查三项外围工作。

## 📝 本轮会话进展
1. **题目拍板**：维持现标题 `Discrimination transports, calibration does not: calibration drift in severity scoring across 187 intensive-care units`；备胎 A/B 只是标题页 HTML 注释，不进提交文件，待办撤销。
2. **审稿人名单 5 人定稿（邮箱全部公开核验）**：
   - van Smeden (UMC Utrecht, M.vanSmeden@umcutrecht.nl) / van Zwet (LUMC, E.W.van_Zwet@lumc.nl) / van de Wiel (Amsterdam UMC, mark.vdwiel@amsterdamumc.nl) — 校准+收缩方法学三连
   - Ryohei Yamamoto (MIT/Fukushima, ryoheiyamamoto11@gmail.com) — MIMIC→eICU 跨库校准、与我们同题
   - Gary Collins (Birmingham, g.s.collins@bham.ac.uk；2025-10 从 Oxford 迁出，投稿当日邮箱再核) — TRIPOD+AI
   - 备胎：Van Calster / Dan Wang / Liu Jianyuan±Gang Liu（邮箱需现场从论文 PDF 核对）
   - 文件：`审稿人推荐_2026-10-21.md`（仓库根权威副本，git 跟踪）＋ `00_投稿包\5_投稿信_Cover_Letter\待选审稿人名单.md`（脚本自动拷入）
   - commit `99da91b`
3. **Yamamoto 2026 预印本全文核对 + 引用落稿**：
   - 出处：Yamamoto R, Wu F, Sprehe LK, Abeer A, Celi LA, Tohyama T. medRxiv 2026.04.05.26350209，2026-04-06 上线，doi:10.64898/2026.04.05.26350209。**无 PMID/无 PMCID**（Europe PMC 仅预印本库 PPR1266483）；PDF 直链 https://www.medrxiv.org/content/medrxiv/early/2026/04/06/2026.04.05.26350209.full.pdf
   - 核对要点：MIMIC-IV 开发 n=30,218 (Sepsis-3, 16.3%) → eICU 208 家外验 n=31,403 (13.9%)；显式不做重校准；逻辑回归校准斜率 1.007→0.417（M1→M7）、ΔAUROC +0.017→−0.125；结论同向："calibration 是迁移性最敏感指标"
   - 落稿位置：Discussion「Relation to prior work on calibration drift」段，"we observed 103 centres simultaneously…" 之后新增一句，新键 `[[YAMAMOTO]]`，装配后参考文献 [14]
   - 新增 REFS 条目于装配_Manuscript.py（ZHANG_TRANSPORT 之后）
4. **全链路重跑九项检查全绿**：装配 76.7KB/1009 行；Results/Methods 数字 ✔；旧数值 0；图注硬编码 ✔；STROBE 引文 54/54；引用编号↔参考文献 **32↔32 零缺漏**；正文词数 **4438/4500（余 62 词）**（Intro 563 + Results 2520 + Discussion 1355）；SciRep 合规 display 6/8；补充材料 0.68MB/11 页；投稿包重建完成。commit `f4f42f8`
5. **投稿包重建防丢失修复**：`整理_投稿包.py` 在 `/整理_投稿包.py:590` 后新增——打包时把仓库根 `审稿人推荐_2026-10-21.md` 自动拷入 `00_投稿包\5_投稿信_Cover_Letter\待选审稿人名单.md`（否则整目录 rmtree 会清掉手写文件）。
6. **同题期刊落点调查（结论：Sci Rep 维持不动）**：
   - 完全同型 MIMIC+eICU 跨库文章的常规落点：Sci Rep（Liu 2024 插管模型）、BMC Gastroenterology、Frontiers in Neurology、Epileptic Disorders、Frontiers in Medicine
   - 方法学一脉：J. Biomed. Inform.（Han 2021）、Artif. Intell. Med.（Zhang lifelong）、Stat Med / SMMR（Ensor、van de Wiel）、BMC Med Res Methodol（Binuya）
   - 我们被拒后的顺位：BMC Med. Inform. Decis. Mak. → J. Biomed. Inform.（需重写为方法学论文）→ PLOS ONE；ICU 大刊与 JAMA IM/LDH/npj 级别因「无部署叙事+三条红线"不可冲
7. **300 例本地 ICU 数据裁定：本篇完全不用**（用户三问确认）：
   - ①数据留给下一篇单独发（学位统计源期刊论文）→ 一稿多用风险
   - ②SOFA 时窗/死亡口径"对不齐/不确定"→ 无法接入 eICU 管线，演示会自曝口径弱点
   - ③伦理是单位质控数据未走流程 → 撑不起新章节
   - 另注意：n≈300 已越过 EB 甜蜜点（200 例后 EB≈朴素重校准，+0.2~+2.0pp），演示价值有限
   - **下篇论文种子**：方向="SOFA 校准漂移在中国 ICU 真实队列 (n≈300) 的表现——单中心纵向观测"；可复用/引用本篇 SciRep 的 EB 固定参数与方法（一环扣一环互引）；前置三件事：口径定死写变量字典、伦理走院级备案/豁免、数据脱敏档案化

## ⚠️ 待解决（全部等用户）
- [ ] 填占位符 5 项：`00_投稿包\6_上传前自查\待填占位符清单.md`（⟨First Author⟩、⟨EMAIL⟩、逐位作者 CRediT、⟨ETHICS⟩ 等）——用户说最后填
- [ ] STROBE checklist 页码（投稿系统要求 n/a 就填 n/a）
- [ ] 审稿人名单最终过目（5 选 4/5，删除或替换随用户）
- [ ] 投稿前统一 `git push`（remote https://github.com/tiantian4634/cross-centre-calibration-drift-icu.git；当前本地领先 origin/main 5 个提交）——可试 `git -c http.proxy= -c https.proxy= push` 直连

## 🔜 下一步
1. 用户填完占位符 → 通知我 → 重跑 `装配_Manuscript.py` + 九项检查 + `组装_补充材料.py` + `整理_投稿包.py` + `质检_投稿包.py`
2. Cover letter 按 `待选审稿人名单.md` 第四节英文段收尾
3. 投稿前 push → 上传 Sci Rep 系统（suggested reviewers 用名单，excluded 可不填或按用户意见）
4. 远期：300 例下篇论文立项（data dictionary 先行）
5. 伏笔：审稿人若要求时域稳定性主图化 → S3 小节后移 §J 后 + 升 Fig.6 免重排路径

## 📁 本轮变更文件
- `00_正文…/Introduction_Discussion.md` — Discussion 加 Yamamoto 引用句
- `装配_Manuscript.py` — REFS 加 YAMAMOTO 条目
- `整理_投稿包.py` — 自动拷入审稿人名单
- `审稿人推荐_2026-10-21.md` — 新建（仓库根权威副本）
- `08_正文/Manuscript.md`、`00_投稿包/**` — 装配稿/投稿包全量再生
- git：`99da91b`、`f4f42f8`（均未推送）
