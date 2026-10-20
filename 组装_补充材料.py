# -*- coding: utf-8 -*-
"""组装 Supplementary Information（单文件 PDF）。

Sci Rep 要求：
  · 单独上传、优先单文件 PDF、≤50 MB
  · 图/表编号为 Supplementary Fig. S1 / Table S1，与正文分开
  · Supplementary Note **不编号**（标题可选）
  · 每张图/表在文件内自带简短标题与图注

实现：python-docx 排版 → Word COM 导出 PDF。
（此前用 PIL 把整页渲染成位图，文字不可选中、无法检索；现改为真文字 + 真表格。）
"""
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
FG = os.path.join(B, "04_图表")
OUT_PDF = os.path.join(B, "Supplementary_Information.pdf")
OUT_DOCX = os.path.join(B, "_si_tmp.docx")

CW = 16.0            # 可用正文宽度 cm（A4 21cm − 2×2.5cm 页边距）
GREY = RGBColor(0x44, 0x44, 0x44)
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


# ── 文本渲染 ──────────────────────────────────────────────
def _tex(s):
    s = re.sub(r"\\(?:mathrm|text)\{([^{}]*)\}", r"\1", s.strip())
    for a, b in [("\\tau", "τ"), ("\\lambda", "λ"), ("\\mu", "μ"), ("\\sigma", "σ"),
                 ("\\ge", "≥"), ("\\le", "≤"), ("\\times", "×"), ("\\cdot", "·"),
                 ("\\log", "log"), ("\\bar a", "ā"), ("\\bar{a}", "ā"),
                 ("\\hat a", "â"), ("\\hat{a}", "â")]:
        s = s.replace(a, b)
    return s.replace("\\", "")


def _math_runs(p, s, size=None):
    """把 `_x` / `^x` 转成真下标/上标，其余按斜体变量排。"""
    i, buf = 0, ""

    def flush():
        nonlocal buf
        if buf:
            r = p.add_run(buf)
            r.italic = True
            if size:
                r.font.size = Pt(size)
            buf = ""

    while i < len(s):
        c = s[i]
        if c in "_^" and i + 1 < len(s):
            flush()
            j = i + 1
            if s[j] == "{":
                k = s.find("}", j)
                tok, i = (s[j + 1:k], k + 1) if k > 0 else (s[j + 1:], len(s))
            else:
                tok, i = s[j], j + 1
            r = p.add_run(tok)
            r.italic = True
            if size:
                r.font.size = Pt(size)
            if c == "_":
                r.font.subscript = True
            else:
                r.font.superscript = True
            continue
        buf += c
        i += 1
    flush()


TOK = re.compile(r"(\$[^$]*\$|\*\*[^*]+\*\*|\*[^*\n]+\*|`[^`]*`)")


def add_md(p, text, size=None, color=None, bold_all=False):
    for tok in TOK.split(text):
        if not tok:
            continue
        if tok.startswith("$") and tok.endswith("$") and len(tok) > 1:
            _math_runs(p, _tex(tok[1:-1]), size)
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            r, txt, b = p.add_run(tok[2:-2]), None, True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r, txt, b = p.add_run(tok[1:-1]), None, False
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            r, txt, b = p.add_run(tok[1:-1]), None, False
            r.font.name = "Consolas"
        else:
            r, txt, b = p.add_run(tok), None, False
        r.bold = bold_all or b
        if tok.startswith("*") and not tok.startswith("**"):
            r.italic = True
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color


def para(text="", size=10.5, color=DARK, space_before=0, space_after=4,
         bold=False, align=None, indent=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    if text:
        add_md(p, text, size=size, color=color, bold_all=bold)
    return p


def heading(text, size=13, space_before=10, space_after=5):
    p = para(text, size=size, space_before=space_before, space_after=space_after, bold=True)
    return p


def add_table(rows, widths=None, font_pt=8.5):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    t = doc.add_table(rows=len(rows), cols=ncol)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    if widths is None:
        widths = [CW / ncol] * ncol
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            c = t.cell(ri, ci)
            c.width = Cm(widths[ci])
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            add_md(p, cell, size=font_pt, bold_all=(ri == 0))
    # 逐列设宽（python-docx 需逐单元格设置才生效）
    for ci, w in enumerate(widths):
        for ri in range(len(rows)):
            t.cell(ri, ci).width = Cm(w)
    return t


# ── 1. 封面 ──────────────────────────────────────────────
p = doc.add_paragraph()
r = p.add_run("Supplementary Information")
r.bold = True
r.font.size = Pt(18)
p.paragraph_format.space_after = Pt(10)

para("Discrimination transports, calibration does not: calibration drift in severity scoring across "
     "187 intensive-care units", size=12.5, space_after=18)

heading("Contents", size=12.5, space_before=6)
CONT = [
    ("Supplementary Fig. S1", "Case-mix ladder: between-centre heterogeneity across nested models"),
    ("Supplementary Fig. S2", "Position of the single-centre MIMIC-IV cohort within the eICU-CRD distribution"),
    ("Supplementary Fig. S3", "Year-to-year stability of the calibration offset within hospitals"),
    ("Supplementary Table S1", "Cohort characteristics"),
    ("Supplementary Table S2", "Between-centre variance estimated under four frameworks"),
    ("Supplementary Table S3", "Sensitivity of the empirical-Bayes result to the choice of variance"),
    ("Supplementary Note", "Prespecified analysis plans: index, chronology and disclosures"),
]
add_table([["Item", "Title"]] + [[a, b] for a, b in CONT], widths=[4.6, CW - 4.6], font_pt=9)

para("", space_after=6)
para("Note on numbering. Supplementary figures and tables are numbered S1, S2 … separately from the "
     "main article. Supplementary Notes are not numbered, in accordance with the journal's "
     "supplementary material policy.", size=9, color=GREY, space_before=6, space_after=10)
para("The analysis plans reproduced in the Supplementary Note were written before the corresponding "
     "analyses were executed. Their file timestamps, an explicit disclosure of one timestamp defect, "
     "and a post-hoc correction to the weighting of the shrinkage target are all included, so that the "
     "reader can verify what was specified before what was run.", size=9, color=GREY)

# ── 2. 三张补充图 ────────────────────────────────────────
LEG = open(os.path.join(B, "图注_legend.md"), encoding="utf-8").read()
LEGS = {}
for blk in re.split(r"\n# ", LEG):
    head = blk.split("\n")[0].strip()
    m = re.match(r"^Supplementary Fig\. S(\d+)$", head)
    if not m:
        continue
    eng = re.search(r"### English legend\s*\n(.*?)(?:\n### |\Z)", blk, re.S)
    if eng:
        LEGS["S" + m.group(1)] = re.sub(r"^>\s?", "", eng.group(1), flags=re.M).strip()

TITLES = {
    "S1": "Supplementary Figure S1. Case-mix ladder: between-centre heterogeneity across nested models.",
    "S2": "Supplementary Figure S2. Position of the single-centre MIMIC-IV cohort within the "
          "eICU-CRD distribution of calibration offsets.",
    "S3": "Supplementary Figure S3. Year-to-year stability of the calibration offset within hospitals.",
}
FILES = {"S1": "SuppFigS1_病例组合阶梯.png",
         "S2": "SuppFigS2_MIMIC在多中心分布中的位置.png",
         "S3": "SuppFigS3_同一中心两年校准偏移的稳定性.png"}

for k in ["S1", "S2", "S3"]:
    doc.add_page_break()
    heading(TITLES[k], size=11, space_before=0, space_after=8)
    fp = os.path.join(FG, FILES[k])
    if not os.path.exists(fp):                    # 文件名容错
        cand = [f for f in os.listdir(FG) if f.startswith("SuppFig" + k) and f.lower().endswith(".png")]
        fp = os.path.join(FG, cand[0]) if cand else fp
    doc.add_picture(fp, width=Cm(CW))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.space_after = Pt(10)
    para(LEGS.get(k, "(legend missing)"), size=9, color=GREY, space_after=6)
print("  [1] 三张补充图已入册")

# ── 3. 三张补充表 ────────────────────────────────────────
tab = open(os.path.join(B, "08_正文", "Tables_表格.md"), encoding="utf-8").read()


def md_rows(txt, name):
    i = txt.find(name)
    if i < 0:
        return None, None
    ls = txt[i:].split("\n")
    start = next((k for k, l in enumerate(ls) if l.strip().startswith("|")), None)
    if start is None:
        return None, None
    end = start
    while end < len(ls) and ls[end].strip().startswith("|"):
        end += 1
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in ls[start:end]]
    rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
    return rows, "\n".join(ls[:end])


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
]
for fname, label, widths in SPECS:
    rows, _ = md_rows(tab, fname)
    if not rows:
        print("  ✘ 未找到 %s" % fname)
        continue
    doc.add_page_break()
    heading(label, size=11, space_before=0, space_after=8)
    add_table(rows, widths=widths, font_pt=8)
    lm = re.search(r"\*\*Supplementary Table S\d+ legend\.\*\*\s*(.*?)(?=\n\n>|\n\n\*\*|\n## |\Z)",
                   tab[tab.find(fname):], re.S)
    para("", space_after=2)
    if lm:
        p = para(size=8.5, color=GREY, space_before=6)
        r = p.add_run("Legend. ")
        r.bold = True
        r.font.size = Pt(8.5)
        _leg = re.sub(r"\s+", " ", lm.group(1)).strip()
        _leg = re.sub(r"\s*-{3,}\s*$", "", _leg).strip()   # 去掉表尾的 --- 分隔线
        add_md(p, _leg, size=8.5, color=GREY)
    else:
        para("(legend missing)", size=8.5, color=RGBColor(0x8B, 0, 0))
print("  [2] 三张补充表已入册")

# ── 4. Supplementary Note ────────────────────────────────
note = open(os.path.join(B, "07_投稿附件", "S1_分析计划汇总与披露.md"), encoding="utf-8").read()
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

    # 表格
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

    # 标题
    m = re.match(r"^(#{1,4})\s+(.*)$", s)
    if m:
        lvl = len(m.group(1))
        heading(re.sub(r"\*\*", "", m.group(2)), size=11.5 if lvl <= 2 else 10.5,
                space_before=10 if lvl <= 2 else 8, space_after=4)
        i += 1
        continue

    # 引用块
    if s.startswith(">"):
        buf = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
            i += 1
        para(" ".join(buf), size=9.5, color=GREY, indent=0.6)
        continue

    # 列表
    m = re.match(r"^[-*]\s+(.*)$", s)
    if m:
        txt = m.group(1)
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.line_spacing = 1.1
        add_md(p, txt, size=9.5)
        i += 1
        continue

    # 普通段落（合并连续行）
    buf = []
    while i < len(lines):
        t = lines[i].strip()
        if not t or t.startswith(("|", "#", ">")) or re.match(r"^[-*]\s+", t):
            break
        buf.append(t)
        i += 1
    para(" ".join(buf), size=9.5)
print("  [3] Supplementary Note 已入册")

# ── 5. 导出 PDF ──────────────────────────────────────────
doc.save(OUT_DOCX)

PS = r"""
param([string]$Docx,[string]$Pdf)
$ErrorActionPreference='Stop'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($Docx, [ref]$false, [ref]$false)
    $d.SaveAs2($Pdf, 17)
    $pages = $d.ComputeStatistics(2)
    $d.Close([ref]$false)
    Write-Output "PAGES=$pages"
} finally { $w.Quit() }
"""
ps = os.path.join(B, "_si_conv.ps1")
open(ps, "w", encoding="utf-8-sig").write(PS)
r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps,
                    "-Docx", OUT_DOCX, "-Pdf", OUT_PDF],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("  [4] Word 导出 %s" % (r.stdout or "").strip())
if r.returncode != 0:
    print("      stderr: %s" % (r.stderr or "")[:400])

sz = os.path.getsize(OUT_PDF)
print("\n  ✔ %s" % os.path.basename(OUT_PDF))
print("    %.2f MB  %s" % (sz / 1048576, "✔ ≤50 MB" if sz <= 50 * 1048576 else "✘ 超 50 MB"))
try:
    import fitz
    d = fitz.open(OUT_PDF)
    print("    pypdf/PDF 页数 %d ｜ 文字可选中：%s"
          % (d.page_count, "✔" if len(d[1].get_text().strip()) > 40 else "✘"))
except Exception as e:
    print("    页数复核跳过：%s" % e)
print("=" * 90)
