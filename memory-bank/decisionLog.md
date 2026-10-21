# Decision Log — 路B

## 2026-10-21

### 决策 1：题目维持现标题不动
- **背景**：投稿系统只能填一个标题；此前误记"两个候选贯穿全稿"
- **选项**：现标题 / 备胎 A（Between-centre calibration drift…）/ 备胎 B（…naive local recalibration makes it worse）
- **决定**：维持 `Discrimination transports, calibration does not: calibration drift in severity scoring across 187 intensive-care units`
- **原因**：唯一同时有反差句式+范围限定（187 家）；Sci Rep 偏爱该风格；样本量亮点留摘要第二句；备胎只是标题页 HTML 注释

### 决策 2：审稿人名单 = 3 方法学家 + MIMIC/eICU 同行 + TRIPOD 把关人（5 人）
- **背景**：用户无推荐，倾向"最近发 MIMIC 论文的人"
- **选项**：泛搜最近 MIMIC 作者 / 三层过滤（对口↔响应率↔无冲突）
- **决定**：van Smeden / van Zwet / van de Wiel / Yamamoto / Collins，全部邮箱公开核验
- **原因**：泛搜命中率低；Yamamoto 经 MIMIC-IV+eICU-CRD 定向检索命中，与我们同题（2026 medRxiv）；地理=NL×3+MIT/JP+UK

### 决策 3：引 Yamamoto 预印本（Discussion 一句 + 新键 [[YAMAMOTO]] → [14]）
- **背景**：撞题 preprint 不引反而显盲；预印本可引（Sci Rep 允许）
- **选项**：不引 / Related work 展开 / Discussion 一句
- **决定**：Discussion calibration drift 段一句带数字（斜率 1.007→0.417），措辞"opposite direction, same verdict"
- **原因**：方向互补（他 MIMIC→eICU，我们 eICU→MIMIC）、口径同构（都不重校准）、引他还能给他本人当审稿人时留好印象

### 决策 4：300 例本地数据不进本篇
- **背景**：用户现成 n≈300 SOFA+死亡数据，问能否助力
- **选项**：A 不进留后用 / B 加"真实单中心演示"段 / C 拆进下篇
- **决定**：档 A+C 复合——本篇零使用；数据归属下篇（用户确认已留作单独发表）
- **原因**：①一稿多用冲突学位论文 ②口径对不齐（SOFA 时窗/死亡口径未定）→ 接入即自曝弱点 ③伦理未走流程 ④ n≈300 已越过 EB 甜蜜点，演示增量小；且正文只余 62 词

### 决策 5：投稿包重建防丢（整理_投稿包.py 自动拷入审稿名单）
- **背景**：00_投稿包/ 被 .gitignore 排除且脚本 rmtree 重建，手写文件会丢
- **选项**：名单只放仓库根 / 只放包内 / 双份+脚本拷贝
- **决定**：仓库根为权威（git 跟踪），脚本打包时 copyfile 进 Cover_Letter 目录
- **原因**：单一事实源 + 包内随取随用 + 重建不丢

### 决策 6（之前轮次维持有效的关键决策，往下不重复记录）
- S3 不升正文；合并图方案 A；EB 数字进图注；三条红线不越界；投放前统一 push
