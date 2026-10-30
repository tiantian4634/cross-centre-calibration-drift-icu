# -*- coding: utf-8 -*-
"""Sci Rep 投稿包 · v1（2026-10-31）
从已定稿产物（00_投稿包 / 08_正文 装配稿）按投稿系统上传槽位分类归集：
  01 主稿件 / 02 主图 / 03 补充材料 / 04 报告清单 / 05 Cover Letter+审稿人 / 06 自查
新产物：成品 Cover_letter.docx+pdf（此前为待写状态）、Suggested_Reviewers.docx。
"""
import io, sys, os, shutil, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

B = os.path.dirname(os.path.abspath(__file__))
SRC_PKG = os.path.join(B, "00_投稿包")
OUT = os.path.join(B, "11_SciRep_投稿包")
os.makedirs(OUT, exist_ok=True)

SUB = {
    "01_Manuscript_主稿件": ["1_稿件_Manuscript\\Manuscript.docx", "1_稿件_Manuscript\\Manuscript.pdf",
                          "1_稿件_Manuscript\\Manuscript_source.md"],
    "02_Main_Figures_主图": ["2_正文图_Main_Figures\\Fig1.png", "2_正文图_Main_Figures\\Fig2.png",
                        "2_正文图_Main_Figures\\Fig3.png", "2_正文图_Main_Figures\\Fig4.png",
                        "2_正文图_Main_Figures\\Fig5.png",
                        "2_正文图_Main_Figures\\PDF\\Fig1.pdf", "2_正文图_Main_Figures\\PDF\\Fig2.pdf",
                        "2_正文图_Main_Figures\\PDF\\Fig3.pdf", "2_正文图_Main_Figures\\PDF\\Fig4.pdf",
                        "2_正文图_Main_Figures\\PDF\\Fig5.pdf"],
    "03_Supplementary_SI": ["3_补充材料_Supplementary\\Supplementary_Information.pdf"],
    "04_Checklists_报告清单": ["4_报告清单_Reporting_Checklist\\STROBE_checklist.docx",
                          "4_报告清单_Reporting_Checklist\\STROBE_checklist.pdf"],
    "05_Cover_Letter_Suggested_Reviewers": [],
    "06_自查_Upload_Guide": ["6_上传前自查\\上传前自查清单.md", "6_上传前自查\\待填占位符清单.md"],
}

for d, files in SUB.items():
    dd = os.path.join(OUT, d)
    os.makedirs(dd, exist_ok=True)
    for f in files:
        src = os.path.join(SRC_PKG, f)
        dst = os.path.join(dd, os.path.basename(f))
        if os.path.exists(src):
            shutil.copy2(src, dst)

# ══════════════════ 1. Cover letter 成品 ══════════════════
COVER_TEXT = [
    ("Mr. Maarten — subject block", None),
    ("SUBJECT: Submission of an original Article to Scientific Reports — "
     "\"Discrimination transports, calibration does not: calibration drift in severity scoring "
     "across 187 intensive-care units\"", 1.0),
    (None, 1.0),
    ("Dear Editors,", 0.0),
    (None, 1.0),
    ("We are pleased to submit the above Article for consideration in Scientific Reports. "
     "Using two publicly available, de-identified intensive-care databases (eICU-CRD v2.0, "
     "208 hospitals; MIMIC-IV v3.1, one academic centre), the study quantifies how the calibration "
     "of three standard severity scores (SOFA, OASIS, SAPS-II) varies across centres while their "
     "discrimination does not, why this drift cannot be removed by local recalibration on small "
     "samples, and how an empirical-Bayes shrinkage strategy recovers that loss and transfers to a "
     "second database without refitting.", 0.0),
    (None, 1.0),
    ("The clinical stake is the assumption that institutional benchmarking by observed-to-expected "
     "ratios is meaningful. Our central result — observed-to-expected mortality spanning 0.69 to 1.54 "
     "across centres under one model, with between-centre I\u00b2 = 75.4% — is a direct "
     "quantification of that assumption, and the 2.0\u20132.6-fold spread of cumulative selection of "
     "highlighted thresholds demonstrates what it means at the bedside. The analysis goes beyond a "
     "symptom report: it partitions the drift into measured case-mix, centre size and temporal "
     "components, translates it into decision-threshold consequences, and delivers a reusable "
     "recalibration strategy with the minimum local sample size quantified.", 0.0),
    (None, 1.0),
    ("Reporting and transparency. The manuscript reports STROBE with the RECORD extension "
     "(checklists attached, and attached to the submission), prespecifies all analyses in a "
     "supplementary note reproduced from two archived, time-stamped plans, and labels confirmatory "
     "versus ntier-estimate analyses accordingly, including two intentionally-reported negative "
     "findings. To keep the description honest: this study does not attribute its findings to "
     "differences in quality of care; the external MIMIC-IV analysis tests transferability of the "
     "shrinkage parameters rather than constituting multicentre external validation of the "
     "strategy; and the recalibration strategy is a statistical recommendation, not a clinical one.",
     0.0),
    (None, 1.0),
    ("Statements. The manuscript is not under consideration elsewhere and has not been posted to a "
     "preprint server (the analysis code is publicly archived at "
     "https://doi.org/10.5281/zenodo.23479141). All authors have read and approved the submission; "
     "there are no competing interests; no external funding was received (the article processing "
     "charge is covered by the authors' institutions). Both databases are de-identified and "
     "redistributable only through PhysioNet under its Data Use Agreement; the study used only "
     "publicly accessible data (training record number in the Ethics section of the Methods), and "
     "the authors' institutional review office confirmed that published consent/ethics review was "
     "not required for this remote secondary analysis. A centre-level table without patient data "
     "and all extraction code are provided so that every number can be reproduced.", 0.0),
    (None, 1.0),
    ("Suggested reviewers, with a conflict-of-interest statement, are appended below and will be "
     "entered in the submission system. We are available for any revision at the editor's "
     "discretion.", 0.0),
    (None, 1.0),
    ("Sincerely, on behalf of all authors,", 0.0),
    (None, 1.0),
    ("Tiantian Zhang (corresponding author)", 0.0),
    ("First Clinical Medical College, Zhejiang Chinese Medical University", 0.0),
    ("tiantian4634@163.com \u00b7 ORCID 0009-0000-2350-8008", 0.0),
]


def build_docx(path, title_size=13):
    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.5)
    sec.left_margin = sec.right_margin = Cm(2.5)
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.paragraph_format.space_after = Pt(2)
    return d


# — Cover letter docx —
CL = os.path.join(OUT, "05_Cover_Letter_Suggested_Reviewers", "Cover_letter.docx")
os.makedirs(os.path.dirname(CL), exist_ok=True)
doc = build_docx(CL)
p0 = doc.add_paragraph()
r0 = p0.add_run("Cover letter — Article submission, Scientific Reports")
r0.bold = True
r0.font.size = Pt(13)
p0.paragraph_format.space_after = Pt(10)

hdr = [
    ("From: Tiantian Zhang, First Clinical Medical College, Zhejiang Chinese Medical University "
     "(corresponding author; tiantian4634@163.com)", 9.5, RGBColor(0x44, 0x44, 0x44)),
    ("Co-author: Junzhi Chu, First Clinical Medical College, Zhejiang Chinese Medical University "
     "(junzhichu@stu.zcmu.edu.cn placeholder — verify before submit)", 9.5, RGBColor(0x99, 0x30, 0x20)),
    ("Date: 2026-10-31", 9.5, RGBColor(0x44, 0x44, 0x44)),
]
for text, size, color in hdr:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    rr = p.add_run(text)
    rr.font.size = Pt(size)
    rr.font.color.rgb = color

SUBMISSION = [
    ("SUBJECT: Submission of an original Article to Scientific Reports — \"Discrimination "
     "transports, calibration does not: calibration drift in severity scoring across 187 "
     "intensive-care units\", by Junzhi Chu and Tiantian Zhang (24 October 2026 draft).", True),
    ("Dear Editors,", False),
    ("We are pleased to submit the above Article for consideration in Scientific Reports. Using two "
     "publicly available, de-identified intensive-care databases (eICU-CRD v2.0, 208 hospitals; "
     "MIMIC-IV v3.1, one academic centre), the study quantifies how the calibration of three standard "
     "severity scores (SOFA, OASIS, SAPS-II) varies across centres while their discrimination does "
     "not, why the drift cannot be removed by naive local recalibration on small samples, and how an "
     "empirical-Bayes shrinkage strategy recovers that loss and transfers to a second database "
     "without refitting.", False),
    ("The clinical stake is the assumption that institutional benchmarking by observed-to-expected "
     "ratios is meaningful. Our central result — observed-to-expected mortality spanning 0.69 to 1.54 "
     "across centres under one model, between-centre I² = 75.4% — directly quantifies that premise, "
     "and the bedside effect is shown by the analysis at a 0.20 decision threshold: the observed "
     "mortality among flagged patients spans 15% to 52% across centres. The study goes beyond "
     "describing the drift: the variation is partitioned into measured case-mix, centre size and "
     "calendar-year components, translated into decision-threshold consequences, and a reusable "
     "recalibration strategy is delivered with the minimum local sample size quantified.", False),
    ("Reporting and transparency. The manuscript reports STROBE with the RECORD extension "
     "(checklists attached), the prespecified analyses superseded from two archived, time-stamped "
     "plans (supplementary note), and four confirmatory analyses are labelled as such — including "
     "two negatively reported findings. We have kept the interpretation inside the data: the "
     "residual between-centre variation is not attributed to any difference in quality of care; the "
     "external MIMIC-IV analysis tests transferability of the shrinkage parameters rather than "
     "multicentre external validation; and the recalibration strategy is a statistical "
     "recommendation, not a clinical one.", False),
    ("Statements. The manuscript is not under consideration elsewhere and has not been posted to a "
     "preprint server (the analysis code is publicly archived at "
     "https://doi.org/10.5281/zenodo.23479141). All authors have read and approved the submission, "
     "declare no competing interests, and received no external funding (the article processing "
     "charge is covered by the authors' institutions). Both databases are de-identified and "
     "accessible only through PhysioNet under a Data Use Agreement; our data-use training record "
     "numbers are stated in the Ethics section of the Methods, and the authors' institutional review "
     "office confirmed that submission of this secondary analysis of published data did not require "
     "additional ethics approval. Extraction code, a centre-level summary table with no patient data "
     "(Supplementary) and all intermediate result files are provided so that every number in the "
     "manuscript can be reproduced.", False),
    ("Suggested reviewers, with a conflict-of-interest statement, are appended below and will be "
     "entered in the submission system. We would be glad to respond to any query or revision at the "
     "editor's discretion.", False),
    ("Sincerely, on behalf of all authors,", False),
    ("Tiantian Zhang (corresponding author), for Junzhi Chu and Tiantian Zhang", False),
    ("First Clinical Medical College, Zhejiang Chinese Medical University, China", False),
    ("tiantian4634@163.com · ORCID 0009-0000-2350-8008", False),
]
for text, bold in SUBMISSION:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    rr = p.add_run(text)
    rr.bold = bool(bold)
    if bold:
        rr.font.size = Pt(11)
doc.add_paragraph()
p = doc.add_paragraph()
rr = p.add_run("Appendix — suggested reviewers (to be entered in the submission system)")
rr.bold = True

REVS = [
    ("Prof. Maarten van Smeden — University Medical Center Utrecht, the Netherlands",
     "M.vanSmeden@umcutrecht.nl — statistician behind sample-size methods (pmsampsize) and "
     "model-validation strategy for clinical prediction models (BMC Medicine 2023)."),
    ("Dr. Erik W. van Zwet — Leiden University Medical Center, the Netherlands",
     "E.W.van_Zwet@lumc.nl — statistical foundations of shrinkage estimation (Stat Med 2021)."),
    ("Prof. Mark A. van de Wiel — Amsterdam University Medical Centers, the Netherlands",
     "mark.vdwiel@amsterdamumc.nl — shrinkage-calibration trade-off in prediction (\"Think before "
     "you shrink\", Stat Methods Med Res 2025)."),
    ("Dr. Ryohei Yamamoto — Massachusetts Institute of Technology, USA / Fukushima Medical "
     "University Hospital, Japan (ryoheiyamamoto11@gmail.com) — cross-database (MIMIC-IV versus "
     "eICU-CRD) external validation and calibration transferability (medRxiv 2026)."),
    ("Prof. Gary S. Collins — University of Birmingham, UK (g.s.collins@bham.ac.uk) — professor of "
     "medical statistics and lead author of the TRIPOD+AI statement; reporting standards for "
     "prediction-model research."),
]
for tup in REVS:
    head, body = tup[0], tup[1]
    if tup[2:]:
        body = body + " " + " ".join(tup[2:])
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    rr = p.add_run(head)
    rr.bold = True
    rr.font.size = Pt(10)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(0.6)
    rr = p.add_run(body)
    rr.font.size = Pt(10)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
rr = p.add_run("Conflict-of-interest statement regarding the suggested reviewers: none of the "
                "suggested reviewers has co-authored with the authors of this manuscript, is "
                "affiliated with the authors' institutions, or has been involved in the design, "
                "analysis, or interpretation of this study.")
rr.font.size = Pt(10)
p2 = doc.add_paragraph()
rr = p2.add_run("No reviewers are excluded at this stage.")
rr.font.size = Pt(10)
doc.save(CL)
print("  ✔ Cover_letter.docx")

# — Suggested reviewers docx —
SR = os.path.join(OUT, "05_Cover_Letter_Suggested_Reviewers", "Suggested_Reviewers.docx")
doc2 = build_docx(SR)
h = doc2.add_paragraph()
r_ = h.add_run("Suggested reviewers — Scientific Reports submission")
r_.bold = True
r_.font.size = Pt(13)
h.paragraph_format.space_after = Pt(8)
intro = ("Five experts in prediction-model calibration, shrinkage methodology, and cross-database "
         "ICU validation, matched to the manuscript topic; none has co-authored with the authors, "
         "is affiliated with our institutions, or took part in the study. Emails are as published "
         "and should be re-verified on the day of submission.")
p = doc2.add_paragraph()
rr = p.add_run(intro)
rr.font.size = Pt(10)
tbl = doc2.add_table(rows=1, cols=4)
tbl.style = "Table Grid"
hdr = tbl.rows[0].cells
for i2, name in enumerate(["#", "Reviewer", "Affiliation / Email", "Relevance"]):
    hdr[i2].text = ""
    rr = hdr[i2].paragraphs[0].add_run(name)
    rr.bold = True
    rr.font.size = Pt(10)
REVS_ROWS = [
    ("1", "Maarten van Smeden", "UMC Utrecht, Julius Center\nM.vanSmeden@umcutrecht.nl",
     "sample-size methods (pmsampsize); BMC Med 2023 model-validity programme"),
    ("2", "Erik W. van Zwet", "Leiden UMC, Biomedical Data Sciences\nE.W.van_Zwet@lumc.nl",
     "statistical foundations of shrinkage (Stat Med 2021)"),
    ("3", "Mark A. van de Wiel", "Amsterdam UMC, Epidemiology & Data Science\nmark.vdwiel@amsterdamumc.nl",
     "\"Think before you shrink\", Stat Methods Med Res 2025"),
    ("4", "Ryohei Yamamoto", "MIT IMES / Fukushima Medical University Hospital\nryoheiyamamoto11@gmail.com",
     "MIMIC-IV vs eICU-CRD external validation, calibration transferability (medRxiv 2026)"),
    ("5", "Gary S. Collins", "University of Birmingham (ex-Oxford EQUATOR)\ng.s.collins@bham.ac.uk",
     "TRIPOD+AI lead author; prediction-model reporting standards"),
]
for row in REVS_ROWS:
    cells = tbl.add_row().cells
    for ci, txt in enumerate(row):
        cells[ci].text = ""
        pp = cells[ci].paragraphs[0]
        pp.paragraph_format.space_before = Pt(1)
        pp.paragraph_format.space_after = Pt(1)
        rr = pp.add_run(txt)
        rr.font.size = Pt(9)
widths = [1.0, 3.4, 6.0, 6.0]
for ci, w in enumerate(widths):
    for row in tbl.rows:
        row.cells[ci].width = Cm(w)
p = doc2.add_paragraph()
rr = p.add_run("Backups (if a suggested reviewer is unavailable): Ben Van Calster (KU Leuven, "
               "calibration paradoxes/ICI); Dan Wang (Research Square 2026, MIMIC-IV+eICU-CRD "
               "liver model, high responsiveness, email unverified); Jianyuan Liu / Gang Liu "
               "(Scientific Reports 2024, MIMIC-IV to eICU-CRD cannulation model — emails via the "
               "paper's correspondence page). No reviewers are excluded.")
rr.font.size = Pt(9)
rr2 = p.add_run("  Conflict note: none of the suggested reviewers has co-authored with the authors, "
                 "is affiliated with the authors' institutions, or was involved in the design, "
                 "analysis, or interpretation of this study.")
rr2.font.size = Pt(9)
doc2.save(SR)
print("  ✔ Suggested_Reviewers.docx")

# ══════════════════ 2. PDF 导出 ══════════════════
exports = [(os.path.abspath(CL.with_name("Cover_letter.docx") if hasattr(CL, "with_name") else os.path.join(os.path.dirname(CL), "Cover_letter.docx")),
            os.path.join(os.path.dirname(CL), "Cover_letter.pdf")),
           (SR, os.path.join(os.path.dirname(SR), "Suggested_Reviewers.pdf"))]
ps1 = r"""
param([string]$Src,[string]$Dst)
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
$d = $w.Documents.Open($Src, [ref]$false, [ref]$false)
$d.ExportAsFixedFormat($Dst, 17)
$d.Close($false)
$w.Quit()
"""
sp = os.path.join(os.environ.get("TEMP", "."), "_pack_ps1.ps1")
open(sp, "w", encoding="utf-8-sig").write(ps1)
for src, dst in exports:
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", sp,
                        src, dst], capture_output=True, text=True)
    ok = os.path.exists(dst)
    print("  ✔ PDF" if ok else "  ✘ PDF", os.path.basename(dst), "(exit=%s)" % r.returncode)
os.remove(sp)

# ══════════════════ 3. README 上传说明 ══════════════════
README = os.path.join(OUT, "06_自查_Upload_Guide", "README_上传说明.md")
open(README, "w", encoding="utf-8", newline="\n").write(
    """# Sci Rep 投稿包 · 上传映射（2026-10-31 生成）

包内文件的来源 = `00_投稿包`（同一构建链的最终产物），数量与大小见各文件。

## 系统槽位 → 文件

| 投稿系统槽位 | 本包文件 | 说明 |
|---|---|---|
| Cover Letter（粘贴/上传） | `05_Cover_Letter_Suggested_Reviewers\\Cover_letter.docx` / `.pdf` | 成品；新邮件式排版，可直接全文粘贴 |
| Suggested Reviewers 字段 | `05_Cover_Letter_Suggested_Reviewers\\Suggested_Reviewers.docx` | 5 位（表格式）+ 无冲突声明；备胎与建议单也在内 |
| Manuscript（主稿件文件） | `01_Manuscript_主稿件\\Manuscript.docx` | Word 版（真文字、真表格）；含标题页/正文/图注附后 |
| Review-Ready PDF（多数编辑喜欢双格式） | `01_Manuscript_主稿件\\Manuscript.pdf` | 22 页，同一排版 |
| Source（可选备份） | `01_Manuscript_主稿件\\Manuscript_source.md` | 装配稿 markdown（防系统编译字体/表格错乱时排查） |
| Figures（图片, 1 个文件 1 图） | `02_Main_Figures_主图\\Fig1–5.png`（另有同名 PDF） | PNG 为主传件；PDF 是印刷矢量版备用 |
| Supplementary Information（单文件） | `03_Supplementary_SI\\Supplementary_Information.pdf` | 15 页：图 S1–S3、表 S1–S6、pseudo 计划全文 |
| 报告清单（不强制，随附） | `04_Checklists_报告清单\\STROBE_checklist.docx` / `.pdf` | 注明 RECORD 也包含在内 |
| 上传前自查 | `06_自查_Upload_Guide\\上传前自查清单.md` / `待填占位符清单.md` | 上传顺序逐项打勾 |

## 上传步骤建议（eJP）
1. Start an Article submission → Article type: Article。
2. Paste/attach Cover Letter（05 文件）。
3. Enter metadata（标题、摘要 [[≤200 词，见 01/Manuscript.docx 首页]]、作者与单位、ORCID）。
4. Upload manuscript（01/Manuscript.docx；一定用 Word 版本上传）。
5. Upload figures（02 的五张 PNG，一次一张，命零零 Fig1..Fig5）。
6. Upload supplementary file（03 的单文件 PDF）。
7. Suggested reviewers：粘贴 05 Suggested_Reviewers.docx 的 5 位（姓名、单位、邮箱）。
8. 报告指南附件可选：04 的 STROBe checklist 以 "Reporting Summary / others" 上传。
9. Ethics/data statements：均已在稿件正文内（Methods 伦理节、Data Availability）——系统字段只需确认。

## 待填/待确认项（上传当天）
- [ ] Cover letter 中 Junzhi Chu 的邮箱为占位（红色标注），提交前核实。
- [ ] Transparent peer review 选项（Sci Rep 可公开审稿记录）——现状未勾选，如需修改在系统 opinion 字段声明。
- [ ] 上传日核对 5 位审稿人的邮箱（表里第 4 位用 gmail，第 5 位 2025 年由 Oxford 迁 Birmingham）。
- [ ] 联系人邮箱 tiantian4634@163.com 有效、投稿系统个人档案已与 ORCID 同步（0009-0000-2350-8008）。
""")

imports = os.path.join(OUT, "06_自查_Upload_Guide")
for f in ["上传前自查清单.md", "待填占位符清单.md"]:
    src = os.path.join(SRC_PKG, "6_上传前自查", f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(imports, f))

# manifest
man = []
man.append("# Files in this package (source → destination)\n")
for d, files in SUB.items():
    for f in files:
        n = os.path.basename(f)
        dst = os.path.join(OUT, d, n)
        if os.path.exists(dst):
            man.append("| %s | %d KB | %s |\n" % (n, os.path.getsize(dst) // 1024, d))
for n in ["Cover_letter.docx", "Cover_letter.pdf", "Suggested_Reviewers.docx", "Suggested_Reviewers.pdf"]:
    p2 = os.path.join(OUT, "05_Cover_Letter_Suggested_Reviewers", n)
    if os.path.exists(p2):
        man.append("| %s | %d KB | 05 (新生成) |\n" % (n, os.path.getsize(p2) // 1024))
open(os.path.join(OUT, "MANIFEST.md"), "w", encoding="utf-8", newline="\n").write("".join(man))
print("  ✔ README/MANIFEST")

# 校验清单输出
n_all = 0
for root, dirs, files2 in os.walk(OUT):
    for f in files2:
        n_all += 1
print("包内文件总数:", n_all)
