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
                   "10_预审版", "逐条回应表_预审稿意见v2.docx")

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


add("Response to the pre-review comments (v2) — point-by-point", size=14, bold=True)
para("Manuscript: Discrimination transports, calibration does not: calibration drift in severity scoring "
     "across 187 intensive-care units.  Date: 2026-10-30.", size=9.5, color=GREY)
para("Method note: every checked item was verified against the manuscript source files, the original "
     "figure raster, the generated PDF text layer, raw statistic files, or the online DOI registry — "
     "not by visual impression. Verdicts: FIXED (defect real, corrected), REBUTTED (defect not present "
     "in the files, with evidence), ACCEPTED (editorial/content change adopted).", size=9, color=GREY)

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

tbl = doc.add_table(rows=1, cols=4)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = tbl.rows[0].cells
for i, htxt in enumerate(["#", "Comment", "Verdict", "Response / evidence"]):
    hdr[i].text = ""
    r = hdr[i].paragraphs[0].add_run(htxt)
    r.bold = True
    r.font.size = Pt(9.5)

for num, comment, verdict, resp in ROWS + [BONUS]:
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
para("Rebuilds after this round: manuscript word count 4,498 / 4,500; abstract 200 / 200; Methods/Results "
     "numeric audits all green (16 + 95 items); citations 32/32; Sci-Rep structural compliance all green; "
     "Figure 5 legend reduced to 348 / 350 words; submission package and integrated pre-review draft both "
     "rebuilt with the corrected Figure 1.", size=9, color=GREY)

doc.save(OUT)
print("✔ 已生成:", OUT)
