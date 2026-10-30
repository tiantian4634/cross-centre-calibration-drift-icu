# -*- coding: utf-8 -*-
"""正文初稿 V4（审阅版·全量整合）：图、表与补充材料一体。

结构 = V3（主页临引用内嵌 Figure 1–5 与 Table 1）
     + Supplementary Information（Supplementary Fig. S1–S3、
       Supplementary Table S1–S3、Supplementary Note 全文），
SI 内容与顺序均镜像 组装_补充材料.py（投稿 SI PDF 的唯一上游）。
渲染升级：真下标/上标（a_h → aₕ 字形、τ² → τ²、â_EB → â(EB下标)）。
输出：10_预审版/正文初稿_v4_审阅版_全量整合.docx / .pdf
不改动任何投稿文件；0_投稿包 仍是唯一投稿源。
"""
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

B = os.path.dirname(os.path.abspath(__file__))
FG = os.path.join(B, "04_图表")
SRC = os.path.join(B, "08_正文", "Manuscript.md")
TAB = os.path.join(B, "08_正文", "Tables_表格.md")
LEG_FILE = os.path.join(B, "图注_legend.md")
NOTE_FILE = os.path.join(B, "07_投稿附件", "S1_分析计划汇总与披露.md")
OUT_DIR = os.path.join(B, "10_预审版")
OUT_DOCX = os.path.join(OUT_DIR, "正文初稿_v4_审阅版_全量整合.docx")
OUT_PDF = os.path.join(OUT_DIR, "正文初稿_v4_审阅版_全量整合.pdf")
os.makedirs(OUT_DIR, exist_ok=True)

CW = 16.0
GREY = RGBColor(0x44, 0x44, 0x44)
RED = RGBColor(0xC0, 0x30, 0x20)
DARK = RGBColor(0x11, 0x11, 0x11)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = sec.bottom_margin = Cm(2.5)
sec.left_margin = sec.right_margin = Cm(2.5)

st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.space_after = Pt(4)
st.paragraph_format.line_spacing = 1.15


# ── 文本渲染（V4：markdown + LaTeX 残留 + 真上下标）────────
def _tex(s):
    s = re.sub(r"\\(?:mathrm|text)\{([^{}]*)\}", r"\1", s.strip())
    for a, b in [("\\tau", "τ"), ("\\lambda", "λ"), ("\\mu", "μ"), ("\\sigma", "σ"),
                 ("\\ge", "≥"), ("\\le", "≤"), ("\\times", "×"), ("\\cdot", "·"),
                 ("\\log", "log"), ("\\bar a", "ā"), ("\\bar{a}", "ā"),
                 ("\\hat a", "â"), ("\\hat{a}", "â")]:
        s = s.replace(a, b)
    return s.replace("\\|", "|").replace("\\", "")


def mathify(s):
    def sub(m):
        x = m.group(1).replace("^2", "²").replace("^*", "*")
        return x.replace("{", "").replace("}", "")
    return re.sub(r"\$([^$]*)\$", sub, s).replace("$", "")


def clean(t):
    return mathify(_tex(t))


SUBSUP = re.compile(
    r"(?<![A-Za-z0-9_])([A-Za-z\u0370-\u03ff\u0100-\u017f]{1,4})[_^]\{?([A-Za-z0-9]{1,6})\}?(?![A-Za-z0-9_])")


def _runs_subsup(p, txt, size, color, bold=False, italic=False):
    """把 _x / ^x 后缀渲染成真下标/上标 run。"""
    pos = 0
    for m in SUBSUP.finditer(txt):
        if m.start() > pos and txt[pos:m.start()]:
            r = p.add_run(txt[pos:m.start()])
            r.bold, r.italic = bold, italic
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
        base, suf = m.group(1), m.group(2)
        r = p.add_run(base)
        r.bold, r.italic = bold, True
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
        r = p.add_run(suf)
        r.bold, r.italic = bold, italic
        r.font.subscript = (m.group(0).find("_") >= 0)
        r.font.superscript = ("^" in m.group(0))
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
        pos = m.end()
    if pos < len(txt):
        r = p.add_run(txt[pos:])
        r.bold, r.italic = bold, italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color


def _emit_runs(p, txt, size, color, bold=False, italic=False, mono=False, bold_all=False):
    for sub in re.split(r"(\*.*?\*)", txt):
        if not sub:
            continue
        inner_ital = italic
        if len(sub) > 2 and sub.startswith("*") and sub.endswith("*") and not sub.startswith("**"):
            sub, inner_ital = sub[1:-1], True
        if mono:
            r = p.add_run(sub)
            r.bold, r.italic = bold or bold_all, italic or inner_ital
            r.font.name = "Consolas"
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
        else:
            _runs_subsup(p, sub, size, color, bold=bold or bold_all, italic=italic or inner_ital)


def add_md(p, s, size=10.5, color=None, bold_all=False):
    for tok in re.split(r"(\*\*.*?\*\*|\*.*?\*|`.*?`)", s):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            _emit_runs(p, tok[2:-2], size, color, bold=True, bold_all=bold_all)
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            _emit_runs(p, tok[1:-1], size, color, italic=True, bold_all=bold_all)
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            _emit_runs(p, tok[1:-1], size, color, mono=True, bold_all=bold_all)
        else:
            _emit_runs(p, tok, size, color, bold_all=bold_all)


def para(text="", size=10.5, color=DARK, space_before=0, space_after=4, bold=False, indent=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    if text:
        add_md(p, text, size=size, color=color, bold_all=bold)
    return p


def heading(text, size=13, space_before=10, space_after=5):
    return para(text, size=size, space_before=space_before, space_after=space_after, bold=True)


def emit_block(block, size=10.5):
    lines = [l.rstrip() for l in block.split("\n")]
    if lines and (lines[0].strip().startswith("## ") or lines[0].strip().startswith("### ")):
        htxt = re.sub(r"^#+\s*", "", lines[0].strip())
        heading(htxt, size=11.5, space_before=10)
        lines = lines[1:]
    if not lines:
        return
    if lines[0].strip().startswith("- "):
        buf = []
        for l in lines:
            ls = l.strip()
            if ls.startswith("- "):
                if buf:
                    para(" ".join(buf), size=size, space_after=5)
                    buf = []
                para("• " + clean(ls[2:]), size=size - 0.5, space_after=3)
            elif ls:
                buf.append(ls)
        if buf:
            para(" ".join(buf), size=size, space_after=5)
        return
    txt = " ".join(l.strip() for l in lines if l.strip())
    para(clean(txt), size=size, space_after=5)


def add_picture_block(png, caption, label):
    heading(label, size=11, space_before=12, space_after=6)
    doc.add_picture(png, width=Cm(CW))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.space_after = Pt(8)
    para(caption, size=9, color=GREY, space_after=10)


def add_table(rows, widths=None, font_pt=8.5):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    if widths is None:
        widths = [CW / ncol] * ncol
    t = doc.add_table(rows=len(rows), cols=ncol)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for ri, row in enumerate(rows):
        for ci in range(ncol):
            c = t.cell(ri, ci)
            c.width = Cm(widths[ci])
            pp = c.paragraphs[0]
            pp.paragraph_format.space_before = Pt(1)
            pp.paragraph_format.space_after = Pt(1)
            pp.paragraph_format.line_spacing = 1.0
            add_md(pp, row[ci], size=font_pt, bold_all=(ri == 0))
    for ci, w in enumerate(widths):
        for ri in range(len(rows)):
            t.cell(ri, ci).width = Cm(w)


def md_rows(txt, name):
    i = txt.find(name)
    if i < 0:
        return None
    ls = txt[i:].split("\n")
    start = next((k for k, l in enumerate(ls) if l.strip().startswith("|")), None)
    if start is None:
        return None
    end = start
    while end < len(ls) and ls[end].strip().startswith("|"):
        end += 1
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in ls[start:end]]
    return [r for r in rows if not all(set(c) <= set("-: ") for c in r)]


# ── 解析装配稿 ────────────────────────────────────────────
ms = open(SRC, encoding="utf-8").read()
tab_src = open(TAB, encoding="utf-8").read()


def section(start, end=None):
    i = ms.find(start)
    if i < 0:
        raise RuntimeError("未找到段落头：" + start)
    j = ms.find(end, i + len(start)) if end else len(ms)
    return ms[i + len(start):j].strip("\n")


title_pg = section("# Title Page", "# Abstract")
abstract = section("# Abstract", "## Introduction")
intro = section("## Introduction", "## Results")
results = section("## Results", "## Discussion")
discussion = section("## Discussion", "## Study design and setting")
methods = section("## Study design and setting", "## References")
refs = section("## References", "## Author contributions")
contr = section("## Author contributions", "## Additional Information")
addinfo = section("## Additional Information", "## Figure legends")
legsec_tabsec = None

# 主图注（供内嵌）
legsec = section("## Figure legends", "## Table 1")
LEGS = {}
parts = re.split(r"\*\*Figure (\d)\*\*", legsec)
for k in range(1, len(parts), 2):
    n = parts[k]
    txt = " ".join(l.strip() for l in parts[k + 1].strip().split("\n") if l.strip())
    LEGS[n] = clean(txt)

FIGFILES = {1: "Fig1_两库筛选流程图.png", 2: "Fig2_判别稳与校准漂.png",
            3: "Fig3_三评分校准漂移对比.png", 4: "Fig4_规模分层与临床影响.png",
            5: "Fig5_重校准与收缩收益.png"}
for f in FIGFILES.values():
    assert os.path.exists(os.path.join(FG, f)), "缺图 " + f

PAT = r"(?:Fig|Figure)s?\.?\s*%s[a-d]?(?![0-9])"


def anchors_in(content):
    ev = []
    for n in FIGFILES:
        m = re.search(PAT % n, content)
        if m:
            p_end = content.find("\n\n", m.start())
            p_end = len(content) if p_end < 0 else p_end + 2
            ev.append((p_end, "fig", n))
    m = re.search(r"\bTable 1\b", content)
    if m:
        p_end = content.find("\n\n", m.start())
        p_end = len(content) if p_end < 0 else p_end + 2
        ev.append((p_end, "tab", None))
    ev.sort(key=lambda e: e[0])
    return ev


def render_section(name, content, embed=True):
    heading(name, size=13, space_before=16, space_after=5)
    if embed:
        ev = anchors_in(content)
    else:
        ev = []
    pos = 0
    for p_end, kind, payload in ev:
        chunk = content[pos:p_end]
        for b in chunk.split("\n\n"):
            if b.strip():
                emit_block(b)
        if kind == "fig":
            png = os.path.join(FG, FIGFILES[payload])
            add_picture_block(png, LEGS[str(payload)], "**Figure %s**" % payload)
        else:
            cap = ("Table 1. Between-centre variation in discrimination and calibration across "
                   "103 intensive-care units, by severity score")
            heading(cap, size=11, space_before=12, space_after=6)
            add_table(md_rows(tab_src, "## Table 1"), widths=[6.4, 3.2, 3.2, 3.2])
            mlg = re.search(r"\*\*Table 1 legend\.\*\*(.*?)(\n\n|\Z)", tab_src[tab_src.find("## Table 1"):], re.S)
            if mlg:
                para(clean(" ".join(l.strip() for l in mlg.group(1).split("\n"))), size=9, color=GREY, space_before=6)
        pos = p_end
    for b in content[pos:].split("\n\n"):
        if b.strip():
            emit_block(b)


# ── 组装 DOCX ────────────────────────────────────────────
para("INTERNAL REVIEW DRAFT · v4 full integration (main text + embedded Figure 1–5 / Table 1 + "
     "complete Supplementary Information) · 2026-10-31",
     size=9.5, color=RED, bold=True, space_after=2)
para("正文初稿 V4 · 审阅版（全量整合）：Figure 1–5 与 Table 1 已嵌入正文引用处；文末附完整补充材料"
     "（Supplementary Fig. S1–S3、Table S1–S3、Supplementary Note 全文，编号与正文分列）。"
     "投稿请以 00_投稿包 为准。", size=9, color=GREY, space_after=14)

heading("Title and authors", size=12.5, space_before=0)
for b_txt in title_pg.split("\n\n"):
    b_txt = " ".join(l.strip() for l in b_txt.split("\n") if l.strip())
    if b_txt:
        para(b_txt, size=10.5)

heading("Abstract", size=12.5, space_before=12)
for b_txt in abstract.split("\n\n"):
    b_txt = " ".join(l.strip() for l in b_txt.split("\n") if l.strip())
    if b_txt:
        para(b_txt, size=10.5)
doc.add_page_break()

for name, content, embed in [("Introduction", intro, False), ("Results", results, True),
                             ("Discussion", discussion, False), ("Methods", methods, False)]:
    render_section(name, content, embed)

heading("References", size=13, space_before=16)
for b_txt in refs.split("\n"):
    b_txt = b_txt.strip()
    if re.match(r"^\[\d+\]", b_txt):
        para(b_txt, size=9.5, space_after=3)

heading("Author contributions", size=12.5, space_before=14)
for b_txt in contr.split("\n\n"):
    b_txt = " ".join(l.strip() for l in b_txt.split("\n") if l.strip())
    if b_txt:
        para(b_txt, size=10)

heading("Additional Information", size=12.5, space_before=14)
for b_txt in addinfo.split("\n\n"):
    b_txt = " ".join(l.strip() for l in b_txt.split("\n") if l.strip())
    if b_txt:
        para(b_txt, size=10)

# ── Supplementary Information（嵌入式，镜像组装_补充材料.py）──
doc.add_page_break()
heading("Supplementary Information", size=15, space_before=0, space_after=2)
para("Integrated review draft — SI figures, tables and the note are numbered separately from the main "
     "article, exactly as in the submission file.", size=9, color=GREY, space_after=10)

# SI 图注解析（同组装脚本）
LEG = open(LEG_FILE, encoding="utf-8").read()
SLEG = {}
for blk in re.split(r"\n# ", LEG):
    headm = re.match(r"^Supplementary Fig\. S(\d+)$", blk.split("\n")[0].strip())
    if not headm:
        continue
    eng = re.search(r"### English legend\s*\n(.*?)(?:\n### |\Z)", blk, re.S)
    if eng:
        body = re.sub(r"^>\s?", "", eng.group(1), flags=re.M).strip()
        txt = " ".join(l.strip() for l in body.split("\n") if l.strip())
        SLEG["S" + headm.group(1)] = clean(txt)

STITLES = {
    "S1": "Supplementary Figure S1. Case-mix ladder: between-centre heterogeneity across nested models.",
    "S2": "Supplementary Figure S2. Position of the single-centre MIMIC-IV cohort within the "
          "eICU-CRD distribution of calibration offsets.",
    "S3": "Supplementary Figure S3. Year-to-year stability of the calibration offset within hospitals.",
}
SFILES = {"S1": "SuppFigS1_病例组合阶梯.png",
          "S2": "SuppFigS2_MIMIC在多中心分布中的位置.png",
          "S3": "SuppFigS3_同一中心两年校准偏移的稳定性.png"}

for k in ["S1", "S2", "S3"]:
    doc.add_page_break()
    heading(STITLES[k], size=11, space_before=0, space_after=8)
    fp = os.path.join(FG, SFILES[k])
    if not os.path.exists(fp):
        cand = [f for f in os.listdir(FG) if f.startswith("SuppFig" + k) and f.lower().endswith(".png")]
        fp = os.path.join(FG, cand[0]) if cand else fp
    doc.add_picture(fp, width=Cm(CW))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.space_after = Pt(10)
    para(SLEG.get(k, "(legend missing)"), size=9, color=GREY, space_after=6)

# SI 表
SPECS = [
    ("## Supplementary Table S1",
     "Supplementary Table S1. Cohort characteristics.",
     [5.6, 2.6, 2.6, CW - 10.8]),
    ("## Supplementary Table S2",
     "Supplementary Table S2. Between-centre variance estimated under four frameworks.",
     [4.9, 2.2, 2.0, 3.0, CW - 12.1]),
    ("## Supplementary Table S3",
     "Supplementary Table S3. Sensitivity of the empirical-Bayes result to the choice of between-centre variance.",
     [2.6, 4.4, 4.4, CW - 11.4]),
    ("## Supplementary Table S4",
     "Supplementary Table S4. Characteristics of the eligible (103) and excluded (84) centres, all 187 hospitals.",
     [5.2, 2.2, 3.4, 2.2, 2.0, CW - 15.0]),
    ("## Supplementary Table S5",
     "Supplementary Table S5. Success rates under the prespecified ±20% band (|O/E − 1| ≤ 0.20), secondary measure.",
     [4.6, 2.2, 2.0, 2.0, 2.0, 2.4, CW - 15.2]),
    ("## Supplementary Table S6",
     "Supplementary Table S6. Variable definitions and coding.",
     [3.0, 3.4, 5.6, CW - 12.0]),
]
for fname, label, widths in SPECS:
    rows = md_rows(tab_src, fname)
    if not rows:
        print("  ✘ 未找到 " + fname)
        continue
    doc.add_page_break()
    heading(label, size=11, space_before=0, space_after=8)
    add_table(rows, widths=widths, font_pt=8)
    lm = re.search(r"\*\*Supplementary Table S\d+ legend\.\*\*\s*(.*?)(?=\n\n>|\n\n\*\*|\n## |\Z)",
                   tab_src[tab_src.find(fname):], re.S)
    para("", space_after=2)
    if lm:
        _leg = re.sub(r"\s+", " ", lm.group(1)).strip()
        _leg = re.sub(r"\s*-{3,}\s*$", "", _leg).strip()
        p = para(size=8.5, color=GREY, space_before=6)
        p.add_run("Legend. ").bold = True
        add_md(p, clean(_leg), size=8.5, color=GREY)

# Supplementary Note（全文渲染：标题/表格/引用/列表/段落）
note = open(NOTE_FILE, encoding="utf-8").read()
note = re.sub(r"^# .*?\n", "", note, count=1)

doc.add_page_break()
heading("Supplementary Note", size=13, space_before=0, space_after=2)
para("Prespecified analysis plans: index, chronology and disclosures", size=10, color=GREY, space_after=10)

lines = note.split("\n")
i = 0
while i < len(lines):
    s = lines[i].strip()
    if not s or re.fullmatch(r"-{3,}", s):
        i += 1
        continue
    if s.startswith("|"):
        blk = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            blk.append(lines[i].strip())
            i += 1
        rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in blk]
        rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
        if rows:
            add_table(rows, font_pt=8)
            para("", space_after=4)
        continue
    m = re.match(r"^(#{1,4})\s+(.*)$", s)
    if m:
        lvl = len(m.group(1))
        heading(re.sub(r"\*\*", "", m.group(2)), size=11.5 if lvl <= 2 else 10.5,
                space_before=10 if lvl <= 2 else 8, space_after=4)
        i += 1
        continue
    if s.startswith(">"):
        buf = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
            i += 1
        para(clean(" ".join(buf)), size=9.5, color=GREY, indent=0.6)
        continue
    m = re.match(r"^[-*]\s+(.*)$", s)
    if m:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.75)
        para("• " + clean(m.group(1)), size=9.5, space_after=2)
        i += 1
        continue
    buf = []
    while i < len(lines) and lines[i].strip() and not re.match(r"^([|#>-]|-{3,}$)", lines[i].strip()):
        buf.append(lines[i].strip())
        i += 1
    if buf:
        para(clean(" ".join(buf)), size=9.5, space_after=5)
    elif not s.startswith(("|", "#", ">", "-", "‣")):
        i += 1

doc.save(OUT_DOCX)
print("  ✔ DOCX:", OUT_DOCX)

ps1 = r"""
param([string]$Docx,[string]$Pdf)
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
$d = $w.Documents.Open($Docx, [ref]$false, [ref]$false)
$d.ExportAsFixedFormat($Pdf, 17)
$d.Close($false)
$w.Quit()
"""
sp = os.path.join(os.environ.get("TEMP", "."), "_v4_export.ps1")
open(sp, "w", encoding="utf-8-sig").write(ps1)
r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", sp, OUT_DOCX, OUT_PDF], capture_output=True, text=True)
print("  DOCX→PDF exit=%s" % r.returncode, (r.stderr or "").strip()[:150])
os.remove(sp)
