# -*- coding: utf-8 -*-
"""生成 STROBE + RECORD 合规审计报告（内部工作审计，非投稿清单）。"""
import io, sys, os, hashlib, datetime, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
SRC = os.path.join(B, "08_正文")
OUT = os.path.join(B, "07_投稿附件", "STROBE_RECORD_合规审计.md")

files = ["TitlePage_标题页.md", "Abstract_摘要_SciRep版.md",
         "Introduction_Discussion.md", "Results.md", "Methods.md", "Tables_表格.md",
         "BackMatter_文末段落.md"]
blob = b"".join(open(os.path.join(SRC, f), "rb").read() for f in files)
sha = hashlib.sha256(blob).hexdigest()[:12]
date = "2026-10-20"

# (编号, 分组, 条目, 状态, 位置, 备注)
R = [
 ("1a","Title and Abstract","Indicate the study design with a commonly used term in the title or abstract","PRESENT","Abstract, sentence 1","'secondary analysis of eICU-CRD' 已补入摘要首句"),
 ("1b","Title and Abstract","Informative and balanced abstract summary","PRESENT","Abstract","200 词、非结构化、含主要结果与两条阴性发现"),
 ("2","Introduction","Scientific background and rationale","PRESENT","Introduction, ¶1–3","严重度评分的用途 → 校准 vs 判别 → 漂移文献综述"),
 ("3","Introduction","Specific objectives, including prespecified hypotheses","PRESENT","Introduction, final ¶","列出四项分析目标与预指定判据引用"),
 ("4","Methods","Key elements of study design early in the paper","PRESENT","Methods §1","'retrospective secondary analysis of two publicly available databases'"),
 ("5","Methods","Setting, locations, relevant dates","PRESENT","Methods §Data sources","eICU 2014–2015 美国 208 家医院；MIMIC-IV 单中心"),
 ("6a","Methods","Eligibility criteria and sources/methods of selection","PRESENT","Methods §Cohort construction + Figure 1","逐步排除标准，计数取自提取阶段的 count 报告"),
 ("6b","Methods","Matching criteria","N/A","—","非匹配设计"),
 ("7","Methods","Define all outcomes, exposures, predictors, confounders","PRESENT","Methods §Variables / §Centre-level calibration measures","院内死亡为结局；a_h、b_h、三评分均给出定义与算法"),
 ("8","Methods","Data sources and details of methods of assessment","PRESENT","Methods §Data sources + §Severity scores","第三方数据库、版本、许可凭证；评分按原始文献定义使用"),
 ("9","Methods","Efforts to address potential sources of bias","PRESENT","Methods §Potential sources of bias","★已补：选择/信息/泄漏/中心间比较的混杂 四类偏倚"),
 ("10","Methods","How the study size was arrived at","PRESENT","Methods §Study size and missing data","★已补：'No sample size calculation was performed' + 全部合格患者纳入"),
 ("11","Methods","How quantitative variables were handled; groupings and why","PRESENT","Methods §Quantitative variables and cut-points","★已补：连续不分类；全部阈值/边界/重抽样次数均为事前固定并指向 S1"),
 ("12a","Methods","All statistical methods including confounding control","PRESENT","Methods §Pooled models … §Statistical reporting","四框架 τ²、LOO 交叉拟合、配对 Wilcoxon、多重性声明"),
 ("12b","Methods","Methods to examine subgroups and interactions","PRESENT","Methods §Centre size and clinical impact","规模三分层；分析为描述性"),
 ("12c","Methods","How missing data were addressed","PRESENT","Methods §Study size and missing data","★关键不可豁免项：唯一缺失变量为 cci 11.6%，仅用于描述性 M3，不插补"),
 ("12d","Methods","How loss to follow-up was addressed","N/A","—","结局为院内死亡，源自住院记录，无失访"),
 ("12e","Methods","Sensitivity analyses","PRESENT","Methods §Between-centre heterogeneity + §Analysis framework","τ² 四框架（分析 K）；病例组合阶梯 M1–M3"),
 ("13a","Results","Numbers at each stage","PRESENT","Results §Cohort; Figure 1","30,796 / 187 家 → 103 家；MIMIC 8,579"),
 ("13b","Results","Reasons for non-participation at each stage","PRESENT","Figure 1 + Methods §Cohort construction","每一步排除的人数与理由"),
 ("13c","Results","Flow diagram","PRESENT","Figure 1","两库筛选流程图"),
 ("14a","Results","Characteristics of participants and confounders","PRESENT","Supplementary Table S1","★表已含缺失数据行"),
 ("14b","Results","Number with missing data for each variable","PRESENT","Supplementary Table S1 + Methods","★已补：仅 cci 缺失 11.6%/0.04%，其余 0%"),
 ("14c","Results","Summarise follow-up time","PRESENT","Methods §Cohort construction","结局窗口为本次住院；入组要求 ICU LOS ≥24 h"),
 ("15","Results","Numbers of outcome events or summary measures","PRESENT","Supplementary Table S1","院内死亡 3,901 (12.7%) / 1,654 (19.3%)"),
 ("16a","Results","Unadjusted/adjusted estimates and precision; which confounders and why","PRESENT","Results §1; Table 1","★已补：合并 AUC 的 95% CI（按医院整群 bootstrap，1000 次）；混协变量的选择理由见 Methods §Case-mix ladder"),
 ("16b","Results","Category boundaries when continuous variables were categorized","PRESENT","Methods §Quantitative variables","★已补：中心规模三分层边界 100–181 / 184–280 / 289–987"),
 ("16c","Results","Translate relative risk into absolute risk","N/A","—","无相对风险估计；本研究直接报告绝对风险与 O/E"),
 ("17","Results","Other analyses: subgroups, interactions, sensitivity","PRESENT","Results §4/§10; Methods","规模分层、τ² 四框架、阶梯"),
 ("18","Discussion","Key results with reference to objectives","PRESENT","Discussion, ¶1","开篇即概括六项发现"),
 ("19","Discussion","Limitations incl. direction and magnitude of bias","PRESENT","Discussion §Limitations","六条局限；Charlson 编码差异已补"),
 ("20","Discussion","Cautious interpretation incl. multiplicity, similar studies","PRESENT","Discussion, 全篇","与既往漂移/更新文献逐篇比较；多重性已在 Methods 说明"),
 ("21","Discussion","Generalisability","PRESENT","Discussion §Limitations, 第六条","两个数据库；对其他卫生系统与评分家族的推广性留白"),
 ("22","Other Information","Source of funding and role of funders","PRESENT","08_正文\\BackMatter_文末段落.md","★已补：'This research received no external funding.'（单位承担版面费亦须在稿件中写明）"),
 # ---- RECORD ----
 ("R 1.1","RECORD — Title/Abstract","Type of data and database name(s) in title or abstract","PRESENT","Abstract","★已补：'secondary analysis of eICU-CRD'、'transferring to MIMIC-IV'"),
 ("R 1.2","RECORD — Title/Abstract","Geographic region and timeframe in title or abstract","PARTIAL","—","摘要未含地域与年份；Methods 已写明（美国、2014–2015）。Sci Rep 无强制，可接受但宜知悉"),
 ("R 1.3","RECORD — Title/Abstract","Linkage between databases stated","N/A","—","两库为独立分析，未做个体级链接"),
 ("R 6.1","RECORD — Methods","Codes/algorithms used to identify study population","PRESENT","Methods §Cohort construction","逐步纳入排除，可复现"),
 ("R 6.2","RECORD — Methods","Validation studies of codes/algorithms referenced","PRESENT","Methods §Validity of the variable definitions","★已补：三评分为已验证并发表的评分，按原始文献使用；死亡为出院状态非算法衍生"),
 ("R 6.3","RECORD — Methods","Linkage flow diagram","N/A","—","无链接"),
 ("R 7.1","RECORD — Methods","Complete list of codes/algorithms for exposures/outcomes/confounders","PRESENT","Methods §Validity + §Centre-level calibration measures","未自研代码表；衍生定义（a_h、b_h）已完整给出"),
 ("R 12.1","RECORD — Methods","Extent of access to the database population","PRESENT","Methods §Data sources","'All database access was read-only' + 全库纳入"),
 ("R 12.2","RECORD — Methods","Data cleaning methods","PRESENT","Methods §Cohort construction + §Missing data","逐步排除；唯一变量级缺失为 cci"),
 ("R 12.3","RECORD — Methods","Linkage methods and quality","N/A","—","无链接"),
 ("R 13.1","RECORD — Results","Selection incl. data-quality/availability/linking filters","PRESENT","Methods + Figure 1","含'三变量全缺失'的数据可用性过滤"),
 ("R 19.1","RECORD — Discussion","Implications of using secondary data: misclassification, unmeasured confounding, missing data, changing eligibility","PRESENT","Discussion §Limitations, 第一条","★已补：点名误分类偏倚（方向与量级无法量化）与随时间变化的纳入标准（受限于仅两年数据）"),
 ("R 22.1","RECORD — Other","Access to protocol, raw data, programming code","PRESENT","Methods §Data availability + Zenodo DOI","代码与计划已归档并有 DOI；须转成正文小节"),
]

C = {}
for _, _, _, s, _, _ in R:
    C[s] = C.get(s, 0) + 1
total = len(R)
na = C.get("N/A", 0)
present = C.get("PRESENT", 0)
pct = 100.0 * present / (total - na)

lines = []
lines.append("<!-- INTERNAL AUDIT — NOT FOR SUBMISSION. This is the /check-reporting working")
lines.append("report, not the official journal checklist. Do not upload to a submission portal. -->\n")
lines.append("# STROBE + RECORD 合规审计报告（内部工作审计）\n")
lines.append("| 项 | 值 |")
lines.append("|---|---|")
lines.append("| 审计日期 | %s |" % date)
lines.append("| 审计范围 | %s |" % ", ".join(files))
lines.append("| 稿件指纹 (source_sha256) | `%s` |" % sha)
lines.append("| 指南 | **STROBE 2007**（基）+ **RECORD 2015**（扩，因使用例行收集的 ICU 电子病历数据）|")
lines.append("| 理由 | eICU-CRD 与 MIMIC-IV 均为**非为本研究目的收集**的例行健康数据 → 触发 RECORD 路由 |\n")
lines.append("## Part A — 汇总\n")
lines.append("| 状态 | 数量 |")
lines.append("|---|---|")
for k in ["PRESENT", "PARTIAL", "MISSING", "N/A"]:
    lines.append("| %s | %d |" % (k, C.get(k, 0)))
lines.append("| **合计** | **%d** |" % total)
lines.append("")
lines.append("**合规率**：PRESENT / (total − N/A) = %d / %d = **%.1f%%**\n" % (present, total - na, pct))
lines.append("### ★ 关键不可豁免项（Critical-item floor）\n")
lines.append("STROBE 观察性研究的不可豁免项：**eligibility/selection；exposure/outcome definitions；")
lines.append("**missing-data handling**；participant flow that reconciles**。\n")
lines.append("| 不可豁免项 | 状态 | 位置 |")
lines.append("|---|---|---|")
lines.append("| Eligibility / selection | **PRESENT** | Methods §Cohort construction; Figure 1 |")
lines.append("| Exposure / outcome definitions | **PRESENT** | Methods §Validity of the variable definitions |")
lines.append("| **Missing-data handling** | **PRESENT** | Methods §Study size and missing data; Suppl. Table S1 | ← **本次审计前为 PARTIAL，已补**")
lines.append("| Participant flow that reconciles | **PRESENT** | Figure 1（计数取自提取阶段报告，非事后重建）|\n")
lines.append("> **四条不可豁免项全部 PRESENT。** 审计前『缺失数据处理』为 PARTIAL（Methods 未报各变量缺失数），")
lines.append("> 本次已实测补齐（唯一缺失变量为 Charlson 指数 11.6%，仅用于描述性 M3）。\n")
lines.append("## Part B — 逐条清单\n")
lines.append("| # | 分组 | 条目 | 状态 | 位置 | 备注 |")
lines.append("|---|---|---|---|---|---|")
for a, b, c, s, loc, note in R:
    lines.append("| %s | %s | %s | **%s** | %s | %s |" % (a, b, c, s, loc, note))
lines.append("")
lines.append("## Part C — 待处理项（仅 MISSING / PARTIAL）\n")
lines.append("| 优先级 | 条目 | 问题 | 建议 | AI 可修 |")
lines.append("|---|---|---|---|---|")
lines.append("| P3 | RECORD 1.2 | 摘要未含地域与年份 | Sci Rep 无强制；已确认**不加**（摘要已 200/200 满额，地域与年份见 Methods §Data sources）| —（作者决定不改）|")
lines.append("")
lines.append("> STROBE 16a（合并 AUC 的 95% CI）与 STROBE 22（Funding）已在本轮补齐，不再列于本表。")
lines.append("> 剩余唯一 PARTIAL 为 RECORD 1.2，属可选项且已由作者决定不改。")
lines.append("")
lines.append("## Part D — 机器可读 JSON\n")
j = {"guideline": ["STROBE 2007", "RECORD 2015"], "target_version": "2026-10-20",
     "source_sha256": sha, "total_items": total, "na_items": na,
     "present": present, "partial": C.get("PARTIAL", 0), "missing": C.get("MISSING", 0),
     "compliance_pct": round(pct, 1),
     "critical_items_all_present": True,
     "action_items": [
         {"item": "RECORD 1.2", "status": "PARTIAL", "fixable_by_ai": False,
          "suggested_fix": "Not applied by author decision: abstract is at the 200-word limit and "
                           "geography/years are reported in Methods. Sci Rep does not require this."}],
     "fixed_this_round": [
         {"item": "STROBE 12c / 14b", "fix": "Missing-data handling quantified; only Charlson "
                                             "index missing (11.6% eICU, 0.04% MIMIC)"},
         {"item": "STROBE 16a", "fix": "95% CI for pooled AUC by cluster bootstrap (1000 replicates)"},
         {"item": "STROBE 22", "fix": "Funding statement added to back matter"},
         {"item": "RECORD 1.1", "fix": "Database names (eICU-CRD, MIMIC-IV) added to abstract"},
         {"item": "RECORD 6.2", "fix": "Validity of variable definitions stated"},
         {"item": "RECORD 19.1", "fix": "Misclassification bias and eligibility drift discussed"}]}
lines.append("```json")
lines.append(json.dumps(j, ensure_ascii=False, indent=2))
lines.append("```")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("  ✔ 已生成 %s" % os.path.basename(OUT))
print("    指纹 %s" % sha)
print("    条目 %d（N/A %d）→ 合规率 %.1f%%" % (total, na, pct))
print("    状态: " + ", ".join("%s=%d" % (k, v) for k, v in C.items()))
print("\n    ★ 关键不可豁免项: 全部 PRESENT（缺失数据处理为本次补齐）")
print("    待处理: RECORD 1.2 (PARTIAL，可选，作者已决定不改)")
print("\n    行数: %d" % (len(lines) + 1))