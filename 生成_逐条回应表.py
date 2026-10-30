# -*- coding: utf-8 -*-
"""逐条回应表：《预审稿意见 v2》 审计结论与处置对照（给预审稿人回信用）。
事实核查方法：装配稿/源文件 grep 全文、Fig1 原图目检、V2 PDF/DOCX 文本层检索、
Zenodo DOI 在线验证、analysis_batch2.py/batch2_results.json/hospital_level_三评分.csv 复算。
"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "10_预审版", "逐条回应表_三轮意见汇总.docx")

DARK = RGBColor(0x11, 0x11, 0x11)
GREY = RGBColor(0x44, 0x44, 0x44)
GREEN = RGBColor(0x1E, 0x6B, 0x2E)
RED = RGBColor(0xB0, 0x30, 0x25)
BLUE = RGBColor(0x1F, 0x4E, 0x79)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = sec.bottom_margin = Cm(2.0)
sec.left_margin = sec.right_margin = Cm(1.8)

st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(9.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.space_after = Pt(3)


def add(text, size=9.5, color=None, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    return p


def para(text="", size=9.5, color=DARK):
    return add(text, size=size, color=color)


add("Response to the pre-review comments — three rounds consolidated", size=14, bold=True)
para("Manuscript: Discrimination transports, calibration does not: calibration drift in severity scoring "
     "across 187 intensive-care units.  Round 1 comments (v2) + Round 2 audit + Round 3 full review "
     "(on the v4 integrated draft).  Date: 2026-10-31.", size=9.5, color=GREY)
para("Method note (unchanged in spirit, upgraded in the second round): every item is verified against the "
     "manuscript source files, the original figure raster, the generated PDF/DOCX text layer, raw "
     "statistic files, or the online DOI registry / OpenAlex records — and, for the contested round-2 "
     "items, additionally by page-level screen renders of the actual PDF (Appendix A), so that arguments "
     "about extraction artifacts can be settled by what a PDF reader displays.", size=9, color=GREY)

ROWS = [
    # M1-M10
    ("M1", "参考文献列表完全缺失", "REBUTTED for the submission file; FIXED in the pre-review draft",
     "The submission manuscript and its DOCX/PDF contain all 32 references in the References section "
     "(automated check: 32 cited /[32] listed, no gaps). The missing list was an artifact of the "
     "integrated pre-review build — its generator matched numbered entries with the wrong pattern. "
     "v3 of the integrated draft reproduces all 32 entries as separate numbered paragraphs."),
    ("M2", "Table 1 排版崩坏，被压缩进单个单元格", "REBUTTED",
     "The pre-review DOCX contains Table 1 as a true 8-row × 4-column Word table (verified cell by "
     "cell: header '…| SOFA | OASIS | SAPS-II', all rows present). The collapse occurred in the "
     "reviewer's PDF-to-text extraction, not in the file. No change needed; millimetre column widths "
     "were kept as reviewed."),
    ("M3", "正文 139,367 vs 图 1 193,367 不一致", "REBUTTED",
     "Direct inspection of the figure raster: the first-box label reads 'First ICU stay per patient "
     "(n = 139,367)', identical to text, legend and cohort/eicu_counts.json. No '193,367' exists "
     "anywhere in the repository. The digit transposition appears to arise in reading the box label."),
    ("M4", "Figure 2 图注顶部混入 '2020- 0.745' 残留", "REBUTTED (residual text); FIXED (LaTeX tokens)",
     "The string '2020- 0.745' (and any '2020…0.745' juxtaposition) appears 0 times in the manuscript, "
     "the legend source, or the PDF text layer. The related point about unreadable $…$ markers in the "
     "integrated draft legends was real for that draft and is fixed in v3: all inline math now renders "
     "as plain text (I², τ², ā, â_EB, ≥ …). The submission files never contained the markers."),
    ("M5", "Figure 3/5 图注大量 LaTeX/\\mathbb{…} 未渲染", "FIXED (in the integrated draft); REBUTTED for \\mathbb",
     "No 'mathbb' string exists in any source or output. The genuine defect was unrendered $I^2$, "
     "$\\tau^2$, $a_h$, $\\bar a$ tokens in the pre-review draft only; the submission already renders "
     "them (HTML→Word chain). The integrated draft v3 renders them natively as I², τ², aₕ-form plain text."),
    ("M6", "Analysis K 'no hypothesis tests' 表述不当；四个显判据分析未列出编号", "ACCEPTED",
     "Methods now reads: 'Analysis K applied a prespecified agreement criterion to point estimates "
     "rather than a formal hypothesis test; the criterion is reported as met or not met.' The four "
     "explicit-criterion analyses are now enumerated as (E, I, J, K) at first mention."),
    ("M7", "Charlson 缺失 11.6% 的 complete-case 论证不足", "PARTIALLY ACCEPTED (reporting now; re-analysis deferred)",
     "Limitations now states: 'The case-mix ladder uses only complete cases (comorbidity missing in "
     "11.6% of eICU patients); the direction of bias is unknown.' The set-sensitivity is already on "
     "record (complete-case M3: n = 27,236, 97 hospitals; I² 70.1% vs 73.5% on the same 97-hospital "
     "subset; see 03_统计/casemix_set_sensitivity.json — case-mix covariates move I² by ~2–3 points). "
     "A missing-indicator variant would require a registered protocol amendment; deferred to the "
     "post-submission round and flagged in the response."),
    ("M8", "MIMIC-IV anchor_age 校正公式未写出", "ACCEPTED",
     "Cohort construction now reads: 'age at admission = anchor_age + (admission year − anchor year)'. "
     "The eICU counterpart (ages >89 recorded as 90) remains stated in Figure 1 and Methods."),
    ("M9", "net benefit 的 treat-all 语境与 TP/FP 分母未写明", "ACCEPTED",
     "Methods now states: 'n is the centre's entire cohort, not only flagged patients; the implicit "
     "comparator is treat-all at the same threshold.' The decision-threshold table (0.10–0.40) and the "
     "PPV-forward framing are unchanged."),
    ("M10", "Calibration slope 模型式与收敛情况缺失", "ACCEPTED",
     "Methods now gives the fitted model as logit(y) = α_h + β_h logit(p̂) with free intercept, and "
     "reports from the deliverable hospital-level file: all 103 slopes per score converged, none "
     "exceeded |β_h| = 5 (largest 2.24, SOFA); slopes >1/<1 are glossed as steeper/compressed gradients."),
    # m1-m10
    ("m1", "摘要 P = 3.7×10⁻¹¹² 复核；请报 effect size", "ACCEPTED (clarified); numbers unchanged",
     "The value is the paired Wilcoxon signed-rank test on identical draws, large-sample normal "
     "approximation; Methods now says so explicitly ('normal approximation'). Effect size is already "
     "reported at every m as paired differences in percentage points (+9.05 at m = 25; +19.0/+15.5/"
     "+13.0/+4.0 at 50/100/200/400), so the extremely small P value is corroborated, not load-bearing. "
     "The statistic is frozen in 03_统计 and re-checked by the regression suite."),
    ("m2", "'15.3% vs 15.5%' 两条成功率的注释位置", "ACCEPTED",
     "The in-text note is removed from Results; the full explanation now lives in Supplementary Item "
     "S1 implementation-disclosure table (row 3). Results keeps one sentence: independent resampling "
     "schemes (100 attempts per cell vs 200 paired draws); comparisons are within, not between, panels."),
    ("m3", "Figure 4b '112 centres' vs 主分析 103 不一致", "ACCEPTED",
     "The net-benefit computation (analysis_batch2.py) screens only on n ≥ 100, giving k = 112 (17.0%/"
     "6.2% negative-net-benefit figures are on exactly these 112). The Figure 4 legend now says: '112 "
     "centres with ≥100 patients — the net-benefit calculation is defined for all of them, including "
     "the 9 centres below the ≥10-death criterion used for the primary between-centre analyses.'"),
    ("m4", "41.6% temporal 成分不可外推为任意两年", "ACCEPTED",
     "Limitations adds: 'The 41.6% temporal share is specific to those two years, not a portable "
     "constant.'"),
    ("m5", "'41.6% temporal in origin' 因果措辞", "ACCEPTED",
     "Discussion now reads: 'A hospital offset of which 41.6% of the variance is temporal cannot be "
     "fully corrected by a permanent recalibration…'"),
    ("m6", "Charlson 3.5 vs 0.9 应在 Results 出现一次", "ACCEPTED",
     "Results, External-application paragraph, now adds: 'MIMIC-IV's higher recorded Charlson index "
     "(3.5 vs 0.9) reflects more complete ICD coding, not case-mix difference; the model has no "
     "comorbidity term.'"),
    ("m7", "λ 需要直观解释", "ACCEPTED",
     "Results adds: 'The shrinkage weight λ is a reliability weight: when SE² dominates τ², λ→0 and "
     "the local estimate collapses to the pooled mean; when τ² dominates, λ→1 and it is retained.'"),
    ("m8", "six-fold 减少需要插值细节与跨 panel 声明", "ACCEPTED (claim verified; sentence added)",
     "The interpolation arithmetic checks out: naive reaches 40.5% at m = 100 and 53.0% at m = 200 "
     "(linear in m: 152 ≈ 100 + 100 × (47.0 − 40.5)/(53.0 − 40.5)); 152/25 ≈ 6 → 'approximately "
     "six-fold'. The new sentence: 'That comparison crosses resampling schemes (Fig. 5c vs 5d) and is "
     "illustrative.'"),
    ("m9", "Figure 5d 在 m = 50 的下凹", "ACCEPTED (quantified; re-run not needed)",
     "From the deliverable raw file, the EB-transfer success rates are 47.0% (m = 25) and 46.0% "
     "(m = 50): the dip is 1.0 percentage point, with SE of a 200-draw rate ≈ 3.5 points (≈0.3 SE), "
     "i.e. comfortably within Monte-Carlo error. The legend now says so with the explicit SE; the "
     "redundant qualitative sentence was removed."),
    ("m10", "STROBE/TRIPOD 段落位置；[23][24] 编号核对", "ACCEPTED",
     "The Discussion paragraph is shortened to its rationale and re-titled 'Reporting standards' "
     "(citations [[TRIPOD_CLUSTER]], [[TRIPOD_AI]], [[STROBE]], [[RECORD]] in the same order). The "
     "citation audit passes at 32/32 with every listed entry cited in reading order, so [23]–[26] "
     "correspondence is verified."),
    # E1-E10
    ("E1", "I²/I^2、τ²/t²、O/E、a_h/a 符号不一致", "FIXED (integrated render); notation clarified",
     "All source text already uses unicode I² and τ²; 't² = 0.131' does not exist in any file. In the "
     "integrated draft the $…$ render fix now makes legends match the body. On a_h vs a: a denotes the "
     "pooled/global calibration offset and a_h the per-hospital offsets — this distinction is "
     "deliberate and is defined at first use ('a_h, the hospital-specific offset'); â marks estimates."),
    ("E2", "图注中 '$…$' 与 'S…S' 混排残留", "FIXED (integrated draft); REBUTTED for 'S…S'",
     "Same root cause as M5: unrendered $…$ in the pre-review build. The 'S…S' pattern has no source; "
     "it is how the reviewer's extractor rendered |$a$|-style delimiters. Submission files are clean."),
    ("E3", "'1. Fig. 3)' 断句残留", "REBUTTED",
     "No such string in the PDF text layer or in any source file."),
    ("E4", "'For sources were considered' 应为 Four", "REBUTTED",
     "Methods reads 'Four sources were considered.' (verified against Methods.md and the PDF layer)."),
    ("E5", "'2020- 0.745' 残留", "REBUTTED",
     "Zero occurrences anywhere (see M4). The only '2020' tokens near that page are reference years."),
    ("E6", "图注 'the m* benchmark' 中 m* 未定义", "ACCEPTED (clarity), chiefly REBUTTED",
     "The legend already reads 'the S0 line is the within-m benchmark (not a learning effect)'; the "
     "'m*' glyph is again an extraction artifact. The sentence was expanded anyway to 'the no-"
     "recalibration rate at that same m (not a learning effect)'."),
    ("E7", "表注 'P, proportion' 应为 I²", "REBUTTED; header suggestion ACCEPTED",
     "The Table 1 note in source and output reads 'I², proportion of total variation attributable to "
     "between-centre heterogeneity.' Optionally, the header was changed per your suggestion to "
     "'Between-centre heterogeneity, I² (%)'."),
    ("E8", "[1]–[32] 编号逐条核对", "ALREADY VERIFIED",
     "The automated audit (run before and after this revision round) confirms: 32 in-text citations, "
     "32 listed entries, none missing, none uncited, numbering follows first occurrence in Reading order."),
    ("E9", "Zenodo DOI 疑似占位", "REBUTTED (verified online)",
     "https://doi.org/10.5281/zenodo.23479141 resolves (HTTP 200) to Zenodo record 23479142, titled "
     "'Cross-centre calibration drift of acute severity scores'. The concept DOI points to the "
     "publicly archived code repository (v1.1). It is live and citable, not a placeholder."),
    ("E10", "图 1 与正文叙述顺序一致性；三处 (n=141)/(n=15) 核对", "REBUTTED (already consistent)",
     "Figure 1 and the Methods narrative follow the same step order: first ICU stay → age ≥65 → "
     "LOS ≥24 h → medical ICU → exclude deaths <24 h → exclude missing outcome status → exclude "
     "albumin/height/weight all missing. The exclusion boxes branch from the fifth box in both "
     "cohorts, matching Methods sentence order. The three numeric mentions (141, 15) agree."),
]

BONUS = ("NEW (found during audit)", "Figure 1: column titles overlapped the blue source-box subtitles",
         "FIXED",
         "The two bold panel titles were drawn over the first box's subtitle row (the raster shows "
         "overprinted text). Root cause: title baseline y = 28.6 vs first box spanning y 27.0–29.4. "
         "Title raised and the main chain lowered by 1.3 units; figure regenerated and re-checked; the "
         "submission package and integrated draft now carry the corrected raster/PDF.")

ROUND2 = [
    ("R2-M3", "核对：Figure 1 图注仍是 193,367", "REBUTTED (page-level evidence)",
     "The '193,367' insists a third time and is again a reading artifact: the assembled Figure 1 legend "
     "in text and on the rendered page (Appendix A-1) reads 'first ICU stay per patient (139,367)'. A "
     "full-text scan of the v3 PDF contains '193,367' 0 times and '139,367' twice (Methods + legend). "
     "The same digit transposition (139→193) recurs across both rounds from the reviewing pipeline."),
    ("R2-M4/E5", "核对：Figure 2 上方仍有 '2020- 0.745)'", "REBUTTED (source string identified)",
     "The reviewing pipeline keeps transcribing the in-figure annotation of Figure 2. Its actual string "
     "is 'pooled AUC 0.732 (95% CI 0.720–0.745)' (Appendix A-2, visible top of the panel; source: "
     "figures_drift.py line 51). '(0.720–' is read as '(2020-'. The token '2020-' occurs 0 times in the "
     "manuscript, the legend source and the PDF text layer; the only '2020' tokens are reference years."),
    ("R2-M2", "核对：v3 的 Table 1 仍是单单元格压缩串", "REBUTTED (page-level evidence)",
     "Appendix A-3 is a screen render of v3 page 4: Table 1 displays as a complete 8-row × 4-column "
     "ruled grid. The '<table>…' string quoted by the reviewing pipeline cannot occur in any PDF; it is "
     "emitted by the pipeline's own HTML export step. The DOCX carries the same true Word table "
     "(verified cell by cell). Submission files unchanged and correct."),
    ("R2-M10", "核对：v3 把斜率模型写成 log(y) = α + β log(p)", "REBUTTED (page-level evidence)",
     "Appendix A-4 (v3 page 16) renders the sentence: 'Within each hospital we fitted logit(y) = α_h + "
     "β_h logit(p̂) with a free intercept and retained β_h. All 103 slopes per score converged; none "
     "exceeded |β_h| = 5 (largest 2.24, SOFA). Slopes above 1 indicate a steeper risk gradient…'. The "
     "PDF text layer contains 'logit(y)' once and 'log(y)' zero times — the 'log(y)' form in the "
     "reviewing pipeline drops the letters 'it' and the hat, so no error exists to correct."),
    ("R2-M1", "核对：文献仍粘连、[2] 缺左括号、24) 缺左括号", "REBUTTED (page-level evidence) + ACCEPTED (DOIs)",
     "Text layer: '[2] Johnson…' occurs verbatim with intact brackets; the PDF renders each of the 32 "
     "entries as its own paragraph (Appendix A-5, page 21). Separately, the reviewer's request to "
     "document the four 2026 references was justified and is now satisfied — see the VAN_GELOVEN row."),
    ("R2-REFS", "四条 2026 年文献需 DOI/PMID 核实", "ACCEPTED — and a real author error found and fixed",
     "All four are real, verified via OpenAlex/Crossref: [13] Zhang Z. et al., Gland Surg. 15, 1274 "
     "(2026), doi:10.21037/gs-2026-0217; [14] Yamamoto R. et al., medRxiv 2026.04.05.26350209, "
     "doi:10.64898/2026.04.05.26350209; [20] Salluh J.I.F. et al., Curr. Opin. Crit. Care 32, 523–530 "
     "(2026), doi:10.1097/mcc.0000000000001411; [22] — the paper exists but was author-misattributed: "
     "the published record is El Arab, R. A., Mustafa, M. H., Almagharbeh, W. T., Saleem, N. H. et al. "
     "(Healthcare 14, 1459 (2026), doi:10.3390/healthcare14111459), not 'van Geloven, N.' The reference "
     "has been corrected and DOIs added to all four entries. Thanks for forcing this verification."),
    ("R2-E1", "核对：t² 与 τ² 混用多处", "REBUTTED",
     "Text layer: 't²' 0 occurrences, 'τ²' 50. The quoted '\\(\\mathrm{t}^2\\) fell from 0.131 to 0.106' "
     "corresponds to the Typeset τ² in 'τ² fell from 0.131 to 0.106' (case-mix ladder section); the τ "
     "glyph plus superscript is read as a latin 't' by the reviewing pipeline. Appendix A-4 shows the "
     "actual typesetting."),
    ("R2-E7", "核对：表注仍为 'P, proportion'", "REBUTTED (page-level evidence)",
     "Appendix A-3 (page 4) — the note reads 'I², proportion of total variation attributable to "
     "between-centre heterogeneity', exactly as round 1 verified at source level. The bold italic 'I²' "
     "glyph is read as 'P' by the pipeline."),
    ("R2-E3", "核对：Page 6 仍有 '1. Fig. 3)'", "REBUTTED",
     "The file context is '…showed heterogeneity of comparable magnitude (Table 1, Fig. 3). Because all "
     "three scores are established…' — clean in source and PDF text layer ('1. Fig. 3)' 0 occurrences). "
     "The '1.' prepended by the pipeline is its own page-boundary artifact (same mechanism in both rounds"),
    ("R2-E6", "核对：m* 字形仍在", "ACCEPTED (de-italicised)",
     "The round-1 rendering set 'within-m' in italics, whose trailing asterisk the pipeline again read "
     "as a superscript marker. The whole phrase is now plain text: 'the S0 line is the within-m "
     "benchmark — the no-recalibration rate at that same m (not a learning effect)'."),
    ("R2-Fig5", "核对：图注用 Δ 与正文 a 两套符号；[a] 应为 |a|", "REBUTTED",
     "The Figure 5 captions use the a-family throughout: ā = +0.030, â_EB = ā + λ(â_ML − ā), λ = τ² / "
     "(τ² + SE²) — same family as Methods. No Δ appears in any caption; the single Δ in the manuscript "
     "is |Δa_h|, the defined year-over-year offset difference of the temporal analysis. 'Residual "
     "miscalibration' is typeset as |a| in text and output; the '[a]' form is the pipeline's bracket "
     "substitution for the vertical bar."),
    ("R2-a_h", "核对：a_{-h} 应为 a_h", "REBUTTED (page-level evidence)",
     "Appendix A-2 (page 5) shows the caption rendering 'Point colour encodes a_h (blue < 0, red > 0)' "
     "and the Figure 3 caption with 'offset a_h'. The '_-h' subscript reading is the pipeline's "
     "subscript transcription; no 'a_{-h}' string exists in any source or output."),
    ("R2-E10", "核对：Figure 1 图注漏掉 (141) 步骤", "ACCEPTED, FIXED",
     "Correct and useful: the legend flow lines jumped from (7)/(363) directly to the analysed cohort "
     "without the (141) step, leaving the arithmetic unexplained in the flow line itself (the Notes "
     "always carried it). Both flow lines now read '… and of missing albumin, height and weight (141)' "
     "(eICU) and '(35) and of missing albumin, height and weight (15)' (MIMIC); the MIMIC age note was "
     "aligned to the new Methods formula ('age at admission = anchor_age + (admission year − anchor "
     "year)'). Legend lengths remain within limits (Figure 1: 305 / 350)."),
    ("R2-QA", "v3 小节标题带出 '### ' 标记（自制证据时发现）", "FIXED",
     "While assembling page renders we caught a genuine layout slip of our own: third-level headings "
     "('### Cohort and study setting' etc.) rendered with the leading marker in the integrated draft "
     "(first-level/second-level were handled). All heading marks are now consumed and render as "
     "formatted headings; a full pass shows 0 residual markers in the rebuilt draft."),
]

EVIDENCE = [
    (r"10_预审版\_证据截图\legend_fig1_flow.png", "A-1 · v3 page 3: Figure 1 legend flow line — 'first ICU stay per patient (139,367)'; no 193,367 anywhere."),
    (r"10_预审版\_证据截图\table1_page.png", "A-3 · v3 page 4: Table 1 rendered as an 8×4 ruled grid; note reads 'I², proportion of total variation…' (rows R2-M2/R2-E7)."),
    (r"10_预审版\_证据截图\fig2_page.png", "A-2 · v3 page 5: Figure 2/3 — in-figure annotation 'pooled AUC 0.732 (95% CI 0.720–0.745)' (source of the ghost string), caption 'Point colour encodes a_h…' (rows R2-M4/R2-a_h)."),
    (r"10_预审版\_证据截图\slope_formula_page.png", "A-4 · v3 page 16: 'logit(y) = α_h + β_h logit(p̂)… All 103 slopes per score converged' (rows R2-M10/R2-E1)."),
    (r"10_预审版\_证据截图\refs_page.png", "A-5 · v3 page 21: references rendered as separate paragraphs, '[2] Johnson…' bracket intact; [13]/[14]/[20]/[22] carry DOIs, [22] corrected to El Arab et al. (rows R2-M1/R2-REFS).")
]

ROUND3 = [
    ("R3-1", "白蛋白/身高/体重全缺失的排除（141/15 例）", "PARTIALLY ACCEPTED — Limitations sentence added after your follow-up",
     "Your follow-up was correct: the Limitations sentence was promised but missing, and it is now in the Limitations (First item): 'The exclusion of patients missing all of albumin, height and weight (141 in eICU-CRD, 15 in MIMIC-IV) was inherited from the source extraction protocol; none of these variables is analysed, but if missingness relates to centre characteristics it could introduce selection bias beyond the 0.46% excluded, and this cannot be assessed from the retained data.' The step itself is prespecified verbatim in the plan and is visible in Figure 1 and Methods; a full characterisation of the excluded patients requires re-derivation upstream of the retained cohort and is offered for the formal revision round."),
    ("R3-2", "84 家被排除中心的特征比较", "ACCEPTED — computed",
     "Supplementary Table S4 (new, post-hoc/exploratory, disclosed in the SI note): the excluded 44.9% are smaller (median 47 patients, IQR 19–78, versus 224, IQR 166–306) and less severely ill (median centre mortality 9.0% versus 12.7%; SOFA 3.48 versus 4.39; ventilated 12.6% versus 23.2%). The eligibility screen therefore over-represents larger, more acute hospitals; the possible direction on the between-centre variance is now discussed in the main text, and no primary number changes."),
    ("R3-3a", "τ² 框架不确定性 → 收缩策略适用范围", "ACCEPTED",
     "The Discussion now states explicitly that with the smaller one-stage τ² = 0.0648 the 25-patient gain narrows from +9.1 to +6.5 points and is undetectable at 200 (Supplementary Table S3), so the guidance is for small local samples under any plausible τ²."),
    ("R3-3b", "自由斜率两阶段 τ² 的敏感性分析", "DEFERRED (this round) — offered",
     "Mechanically feasible with the retained analysis cohort and offered for the formal revision round; it would need to be labelled a post-hoc framework sensitivity (the prespecified plan fixed slope = 1 by design, which is precisely the mechanism in question). All four confirmatory analyses' statuses are reported as-is."),
    ("R3-4", "收缩目标 (+0.030) 与真实偏移 (+0.221) 的差距", "ACCEPTED",
     "Added to the Discussion: the MIMIC-IV target sat ≈ 1.5 τ below the true offset, yet with a raw local SE of ≈ 0.5 at 25 patients (λ ≈ 0.33) the variance reduction outweighed the target bias — the situation expected when moving between databases. This strengthens rather than weakens the strategy's interpretation, as the reviewer anticipated."),
    ("R3-5", "大中心高异质性的机制", "PARTIALLY ACCEPTED",
     "A Discussion paragraph lists candidate mechanisms (care-practice diversity, detection limits) and adds one honest descriptor: per-centre SOFA dispersion is similar across size tertiles (median SD 2.7/3.2/3.1), arguing against a pure case-mix-width account. The 'less complete data quality in small centres may mask drift' direction is stated; a mechanistic causal analysis is out of scope for a descriptive secondary analysis."),
    ("R3-6", "净获益的临床解释", "ACCEPTED",
     "The Methods point is already limited (n = whole centre; treat-all comparator). Added: Results now also report the positive share (positive in the remainder); the Discussion states that negative net benefit speaks only to the treat-all comparator at that threshold, not to clinical worth in general."),
    ("R3-7", "校准偏移 SE 公式", "ACCEPTED — formula verified and rewritten",
     "Re-derivation confirmed the implement ed formula is the textbook delta method: se(a_h) = sqrt(ȳ(1−ȳ)/n_h)/w̄, with ȳ the centre's observed mortality rate and w̄ = mean(p(1−p)). The confusion came from denoting observed mortality by 'ŷ'; the formula section now derives it explicitly (dȳ/da_h = w̄) and uses ȳ throughout."),
    ("R3-8", "±10% / ±20% 标准的依据与 ±20% 结果", "ACCEPTED — computed (prespecification discovered)",
     "The ±20% band was a prespecified secondary measure in the analysis plans ('一并报'), unreported in the text — our own omission. It is now reported in full as Supplementary Table S5 and in Results: at ±20% naive recalibration at 25 patients remains worse than no recalibration (30.6% versus 41.7%), the EB advantage is undiminished (47.9% versus 31.0%; transfer 82.0% versus 42.0%), and the prespecified 50% target applies only to the primary ±10% band."),
    ("R3-9", "41.6% 的限定", "ACCEPTED",
     "The Discussion citation now reads '41.6% of the variance is temporal in those two consecutive years'; the Limitations qualifier was already in place."),
    ("R3-10", "Figure 5 拆分", "PARTIALLY REJECTED — legend restructured instead",
     "Panel d belongs to the confirmatory analysis J; demoting it to supplementary would remove one prespecified negative/positive result from primary view. The single-figure form is kept, and the Question 10 concern about density is handled by the legend's per-panel sub-questions. If the journal also asks for a split, fig 5 would divide cleanly into naive (a–b) and shrinkage (c–d) halves."),
    ("R3-11", "TRIPOD-Cluster 要素;", "ACCEPTED",
     "Reporting standards now names them: the clustering level, the centres per estimate, the centre-level eligibility and the resampling design are all reported, and the standards were matched to the study object rather than avoided."),
    ("R3-12", "SI 中文计划翻译", "PARTIALLY ACCEPTED",
     "(b) The submission SI already carries an English title/description for every referenced plan (SI Note); (a) full parallel translation is offered for the formal revision round: it is a large, verification-heavy artefact, and the 'translation is for access, the Chinese original stays the authoritative record' boundary was set deliberately."),
    ("R3-13", "MIMIC-IV >89 岁处理", "ACCEPTED (one sentence added)",
     "Cohort text now states: ages above 89 are recorded as 91 at the anchor year in MIMIC-IV, so very old ages are censored similarly in the two databases (MIMIC-IV citation already present)."),
    ("R3-14/15/16", "决策阈值依据 / Charlson→J / 统计细节", "ACCEPTED (small edits)",
     "Thresholds: 'chosen to span the operating range of usual risk-stratification decisions'. Limitations: the Charlson/recording-practice difference is stated as a systematic difference that may extend to unmeasured dimensions, so the MIMIC-IV offset cannot be attributed wholly to one source. Statistics: no multiplicty revision needed beyond the existing statement; all 103 slopes converge (already reported as |β_h| ≤ 2.24)."),
    ("R3-17", "medRxiv 引用格式与首页版式", "NO CHANGE; rebutted as a review-build property",
     "The DOI form 'doi:10.64898/2026.04.05.26350209' is the journal-standard medRxiv citation. The 'supplementary S1-3 all integrated / internal note' line is the top-page banner of the integrated REVIEW build used for this pre-review; it does not exist in the submission files (00_投稿包 quality control page-order verified)."),
    ("R3-extension", "给作者非强制建议 (SOFA=8 床旁图 / 随机效应排名)", "NOTE + one discussion move",
     "Both are worthwhile for the revision round: the SOFA=8 cross-centre prediction-mortality figure is computable from the same per-centre offsets already on file; and the residual-variation benchmarking operational suggestion (report O/E intervals / random-effects ranking) is folded into the benchmarking paragraph in spirit via the 'quantity to be monitored' framing. Center-level variable listing: the Data Availability statement already enumerates the centre-level table columns (n, deaths, observed and expected rates, O/E, calibration offset and standard error, per-centre AUC and calibration slope, one row per eligible centre per score), and variable definitions and coding are now consolidated in Supplementary Table S6."),
]
EVIDENCE = EVIDENCE  # 保留两轮截图

tbl = doc.add_table(rows=1, cols=4)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = tbl.rows[0].cells
for i, htxt in enumerate(["#", "Comment", "Verdict", "Response / evidence"]):
    hdr[i].text = ""
    r = hdr[i].paragraphs[0].add_run(htxt)
    r.bold = True
    r.font.size = Pt(9.5)

for num, comment, verdict, resp in ROWS + [BONUS] + ROUND2 + ROUND3:
    cells = tbl.add_row().cells
    for ci, txt in enumerate((num, comment, verdict, resp)):
        cells[ci].text = ""
        pp = cells[ci].paragraphs[0]
        pp.paragraph_format.space_before = Pt(1)
        pp.paragraph_format.space_after = Pt(1)
        r = pp.add_run(txt)
        r.font.size = Pt(8.5)
        if ci == 0:
            r.bold = True
            r.font.color.rgb = BLUE
        if ci == 2:
            if "REBUTTED" in txt and "FIXED" not in txt and "ACCEPTED" not in txt:
                r.font.color.rgb = RED
            elif txt.startswith(("FIXED", "ACCEPTED")):
                r.font.color.rgb = GREEN
    widths = [1.0, 3.6, 3.0, 9.6]

for ci, w in enumerate(widths):
    for row in tbl.rows:
        row.cells[ci].width = Cm(w)

para("")
add("Rebuilds after this round: manuscript word count 4,500 / 4,500; abstract 200 / 200; Methods/Results "
    "numeric audits all green (16 + 95 items); citations 32/32; Sci-Rep structural compliance all green; "
    "Figure legends 305 / 347 words (limit 350); SI rebuilt at 14 pages with the new Supplementary "
    "Tables S4/S5 and two additional SI disclosure rows; both the submission and integrated-review builds refreshed.",
    size=9, color=GREY)

add("Appendix A — page-level screen renders of the revised integrated draft (PDF pages as displayed)",
    size=12, bold=True,
)
for png, cap in EVIDENCE:
    if os.path.exists(png):
        doc.add_picture(png, width=Cm(16.2))
        para(cap, size=8.5, color=GREY)
    else:
        para("(缺少截图：" + png + ")", size=9, color=RED)

doc.save(OUT)
print("✔ 已生成:", OUT)
