# -*- coding: utf-8 -*-
"""正文初稿 V2（预审集成版）：Figure 1–5 与 Table 1 按正文首次引用位置嵌入，
生成给预审稿人看的单文件 DOCX/PDF。

数据源 = 装配稿 08_正文/Manuscript.md（唯一权威），图 = 04_图表/FigN_*.png，
表 = 装配稿 ## Table 1 节。渲染：python-docx 真文字 + Word COM 导出 PDF。
输出：10_预审版/正文初稿_v2_预审版.docx / .pdf
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
OUT_DIR = os.path.join(B, "10_预审版")
OUT_DOCX = os.path.join(OUT_DIR, "正文初稿_v3_预审修订版.docx")
OUT_PDF = os.path.join(OUT_DIR, "正文初稿_v3_预审修订版.pdf")
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


def _tex(s):
    s = re.sub(r"\\(?:mathrm|text)\{([^{}]*)\}", r"\1", s.strip())
    for a, b in [("\\tau", "τ"), ("\\lambda", "λ"), ("\\mu", "μ"), ("\\sigma", "σ"),
                 ("\\ge", "≥"), ("\\le", "≤"), ("\\times", "×"), ("\\cdot", "·"),
                 ("\\log", "log"), ("\\bar a", "ā"), ("\\bar{a}", "ā"),
                 ("\\hat a", "â"), ("\\hat{a}", "â")]:
        s = s.replace(a, b)
    return s.replace("\\|", "|").replace("\\", "")


def mathify(s):
    """$...$ LaTeX 残留 → 可读文本（I² / τ² / ā / â_EB / ≥ …）。"""
    def sub(m):
        x = m.group(1)
        x = x.replace("^2", "²").replace("^*", "*")
        return x.replace("{", "").replace("}", "")
    s = re.sub(r"\$([^$]*)\$", sub, s)
    return s.replace("$", "")


def clean(t):
    return mathify(_tex(t))


def add_md(p, s, size=10.5, color=None, bold_all=False):
    for tok in re.split(r"(\*\*.*?\*\*|\*.*?\*|`.*?`)", s):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            r = p.add_run(tok[2:-2])
            r.bold = True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r = p.add_run(tok[1:-1])
            r.italic = True
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            r = p.add_run(tok[1:-1])
            r.font.name = "Consolas"
        else:
            r = p.add_run(tok)
        r.bold = r.bold or bold_all
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color


def para(text="", size=10.5, color=DARK, space_before=0, space_after=4, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        add_md(p, text, size=size, color=color, bold_all=bold)
    return p


def heading(text, size=13, space_before=10, space_after=5):
    return para(text, size=size, space_before=space_before, space_after=space_after, bold=True)


def emit_block(block, size=10.5):
    """一个 \n\n 段块 → docx 段落（含小节标题/列表识别）。"""
    lines = [l.rstrip() for l in block.split("\n")]
    if lines and lines[0].strip().startswith("## "):
        heading(lines[0].strip()[3:], size=11.5, space_before=10)
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


def add_table(rows, widths, font_pt=8.5):
    t = doc.add_table(rows=len(rows), cols=len(widths))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for ri, row in enumerate(rows):
        row = list(row) + [""] * (len(widths) - len(row))
        for ci in range(len(widths)):
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
    ls = txt[i:].split("\n")
    start = next(k for k, l in enumerate(ls) if l.strip().startswith("|"))
    end = start
    while end < len(ls) and ls[end].strip().startswith("|"):
        end += 1
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in ls[start:end]]
    return [r for r in rows if not all(set(c) <= set("-: ") for c in r)]


# ── 解析装配稿 ────────────────────────────────────────────
ms = open(SRC, encoding="utf-8").read()


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
legsec = section("## Figure legends", "## Table 1")
tab1sec = section("## Table 1")

# 图注（合并软换行；保留 ** 标记供 add_md 渲染）
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


def anchors_in(content, label):
    """[(插入位置(段落结尾之后), kind, payload)]，按位置排序。"""
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
    return ev, content


def render_section(name, content, embed=True):
    heading(name, size=13, space_before=16, space_after=5)
    if embed:
        ev, content = anchors_in(content, name)
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
            cap = "Table 1. Between-centre variation in discrimination and calibration across " \
                  "103 intensive-care units, by severity score"
            heading(cap, size=11, space_before=12, space_after=6)
            add_table(md_rows(ms, "## Table 1"), widths=[6.4, 3.2, 3.2, 3.2])
            lg = re.search(r"\*\*Table 1 legend\.\*\*(.*?)(\n\n|\Z)",
                           tab1sec[tab1sec.find("**Table 1 legend.**"):], re.S)
            if lg:
                para(" ".join(l.strip() for l in lg.group(1).split("\n")),
                     size=9, color=GREY, space_before=6)
        pos = p_end
    for b in content[pos:].split("\n\n"):
        if b.strip():
            emit_block(b)


# ── 组装 DOCX ────────────────────────────────────────────
para("INTERNAL PRE-REVIEW DRAFT · v3 revised (figures & tables embedded) · 2026-10-30",
     size=9.5, color=RED, bold=True, space_after=2)
para("正文初稿 V3 · 预审修订版（已吸收预审稿意见 v2）：Figure 1–5 与 Table 1 已按正文首次引用位置嵌入。"
     "投稿版请以 00_投稿包 为准。", size=9, color=GREY, space_after=14)

heading("Title and authors", size=12.5, space_before=0)
for b in title_pg.split("\n\n"):
    b = " ".join(l.strip() for l in b.split("\n") if l.strip())
    if b:
        para(b, size=10.5)

heading("Abstract", size=12.5, space_before=12)
for b in abstract.split("\n\n"):
    b = " ".join(l.strip() for l in b.split("\n") if l.strip())
    if b:
        para(b, size=10.5)
doc.add_page_break()

for name, content, embed in [("Introduction", intro, False), ("Results", results, True),
                      ("Discussion", discussion, False), ("Methods", methods, False)]:
    render_section(name, content, embed)

heading("References", size=13, space_before=16)
for b in refs.split("\n"):
    b = b.strip()
    if re.match(r"^\[\d+\]", b):
        para(b, size=9.5, space_after=3)

heading("Author contributions", size=12.5, space_before=14)
for b in contr.split("\n\n"):
    b = " ".join(l.strip() for l in b.split("\n") if l.strip())
    if b:
        para(b, size=10)

heading("Additional Information", size=12.5, space_before=14)
for b in addinfo.split("\n\n"):
    b = " ".join(l.strip() for l in b.split("\n") if l.strip())
    if b:
        para(b, size=10)

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
sp = os.path.join(os.environ.get("TEMP", "."), "_v2_export.ps1")
open(sp, "w", encoding="utf-8-sig").write(ps1)
r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", sp, OUT_DOCX, OUT_PDF], capture_output=True, text=True)
print("  DOCX→PDF exit=%s" % r.returncode, (r.stderr or "").strip()[:150])
os.remove(sp)
