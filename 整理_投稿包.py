# -*- coding: utf-8 -*-
"""整理投稿包：把 Sci Rep 需要上传的文件按「上传槽位」分类归集。

设计原则
--------
1. **不改动现有工作目录结构** —— 03_统计 / 04_图表 / 08_正文 等脚本引用的路径全部保持原样，
   避免把整条流水线搞坏。投稿包是**派生产物**，从源文件重新生成。
2. 包内只放**投稿要交的东西**，并按投稿系统的上传槽位分文件夹。
3. 每次重跑会清空重建，所以包内不要手改；要改就改 08_正文 源文件再重跑本脚本。

转换链：Manuscript.md → HTML → Word COM → DOCX（可编辑，表格为真 Word 表）→ PDF
"""
import io, sys, os, re, shutil, subprocess, html as _html, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
PKG = os.path.join(B, "00_投稿包")
SRC = os.path.join(B, "08_正文")

D = {
    "manu": os.path.join(PKG, "1_稿件_Manuscript"),
    "figs": os.path.join(PKG, "2_正文图_Main_Figures"),
    "figp": os.path.join(PKG, "2_正文图_Main_Figures", "PDF"),
    "supp": os.path.join(PKG, "3_补充材料_Supplementary"),
    "chk":  os.path.join(PKG, "4_报告清单_Reporting_Checklist"),
    "cl":   os.path.join(PKG, "5_投稿信_Cover_Letter"),
    "self": os.path.join(PKG, "6_上传前自查"),
}

# ── 清空重建 ────────────────────────────────────────────────
if os.path.isdir(PKG):
    shutil.rmtree(PKG)
for d in D.values():
    os.makedirs(d, exist_ok=True)
print("  [1] 目录结构已建立")

# ── Markdown → HTML ────────────────────────────────────────
def esc(s):
    return _html.escape(s, quote=False)


_GREEK = [("\\tau", "τ"), ("\\lambda", "λ"), ("\\mu", "μ"), ("\\sigma", "σ"),
          ("\\ge", "≥"), ("\\le", "≤"), ("\\times", "×"), ("\\cdot", "·"),
          ("\\log", "log"), ("\\bar a", "ā"), ("\\bar{a}", "ā"),
          ("\\hat a", "â"), ("\\hat{a}", "â")]


def _math(expr):
    """把 $...$ 的 LaTeX 子集渲染成 HTML（下标/上标/希腊字母）。"""
    s = re.sub(r"\\(?:mathrm|text)\{([^{}]*)\}", r"\1", expr.strip())
    for k, v in _GREEK:
        s = s.replace(k, v)
    s = s.replace("\\", "")
    s = re.sub(r"([A-Za-z\u00c0-\u024f\u03b1-\u03c9])_\{([^{}]+)\}", r"\1<sub>\2</sub>", s)
    s = re.sub(r"([A-Za-z\u00c0-\u024f\u03b1-\u03c9])_([A-Za-z0-9*])", r"\1<sub>\2</sub>", s)
    s = re.sub(r"\^\{([^{}]+)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"\^([A-Za-z0-9*])", r"<sup>\1</sup>", s)
    return "<i>%s</i>" % s


def inline(s):
    # 1) 保护转义字符与代码段，避免被 * 和 _ 规则误伤
    s = s.replace("\\|", "\x01PIPE\x01").replace("\\*", "\x01STAR\x01")
    store = []

    def _code(m):
        store.append(m.group(1))
        return "\x02CODE%d\x02" % (len(store) - 1)

    s = re.sub(r"`([^`]+?)`", _code, s)

    # 2) 转义 HTML，再渲染 $...$ 行内公式
    #    （渲染结果含 <i>/<sup> 和字面 *，若直接留在串里会被后面的斜体规则当成定界符，
    #      故先换成占位符，等粗斜体处理完再还原）
    s = esc(s)
    maths = []

    def _math_keep(m):
        maths.append(_math(m.group(1)))
        return "\x03MATH%d\x03" % (len(maths) - 1)

    s = re.sub(r"\$([^$\n]{1,120}?)\$", _math_keep, s)

    # 3) 下标：*a_h* 与 *a*_EB 两种写法
    s = re.sub(r"\*([A-Za-z\u00c0-\u024f\u03b1-\u03c9]+)_([A-Za-z0-9]+)\*",
               r"<i>\1</i><sub>\2</sub>", s)
    s = re.sub(r"\*([A-Za-z\u00c0-\u024f\u03b1-\u03c9]+)\*_([A-Za-z0-9]+)",
               r"<i>\1</i><sub>\2</sub>", s)

    # 4) 粗体、斜体
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<i>\1</i>", s)

    # 5) 正文中裸写的下标（a_h / n_h），代码段已保护
    for v in ("a_h", "n_h"):
        s = re.sub(r"(?<![\w>])%s(?![\w<])" % v,
                   "<i>%s</i><sub>%s</sub>" % (v[0], v[2:]), s)

    # 6) 作者待填占位符 ⟨…⟩ 高亮，便于在 Word 里一眼找到
    s = re.sub(r"⟨[^⟩]*⟩", lambda m: "<span style='background:#FFEB3B'>%s</span>" % m.group(0), s)

    # 7) 还原保护区
    s = s.replace("\x01PIPE\x01", "|").replace("\x01STAR\x01", "*")
    s = re.sub(r"\x03MATH(\d+)\x03", lambda m: maths[int(m.group(1))], s)
    s = re.sub(r"\x02CODE(\d+)\x02",
               lambda m: "<span style='font-family:Consolas,monospace'>%s</span>" % store[int(m.group(1))], s)
    return s


def re_split_row(r):
    """按 | 切分表格行。"""
    r = r.strip()
    if r.startswith("|"):
        r = r[1:]
    if r.endswith("|"):
        r = r[:-1]
    return r.split("|")


def _is_sep_row(t):
    t = t.strip()
    if not t.startswith("|"):
        return False
    cells = [c.strip() for c in re_split_row(t)]
    if not cells or not any(cells):
        return False
    return all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def _is_table_start(lines, i):
    """只有「|…| 开头且下一行是分隔行」才算表格 —— 避免把正文里的 |Δa_h| 当成表格。"""
    return (i + 1 < len(lines) and lines[i].strip().startswith("|")
            and _is_sep_row(lines[i + 1]))


CSS = """body{font-family:'Times New Roman',serif;font-size:12pt;line-height:1.5;}
h1{font-size:15pt;font-weight:bold;margin:18pt 0 8pt 0;}
h2{font-size:13pt;font-weight:bold;margin:14pt 0 6pt 0;}
h3{font-size:12pt;font-weight:bold;font-style:italic;margin:12pt 0 4pt 0;}
p{margin:0 0 8pt 0;text-align:left;}
table{border-collapse:collapse;width:100%;margin:6pt 0 10pt 0;font-size:9.5pt;}
th,td{border:0.75pt solid #000;padding:2.5pt 4pt;vertical-align:top;}
th{font-weight:bold;background:#F2F2F2;}
blockquote{margin:6pt 0 8pt 24pt;font-style:italic;}
hr{border:none;border-top:0.75pt solid #999;margin:10pt 0;}
"""


def md_to_html(md):
    out, i = [], 0
    lines = md.split("\n")
    n = len(lines)
    listbuf = []

    def flush_list():
        nonlocal listbuf
        if listbuf:
            out.append("<ul style='margin:4pt 0 8pt 18pt'>")
            for it in listbuf:
                out.append("<li>%s</li>" % inline(it))
            out.append("</ul>")
            listbuf = []

    while i < n:
        ln = lines[i]
        s = ln.strip()

        if not s:
            flush_list()
            i += 1
            continue

        # 分隔线
        if re.fullmatch(r"-{3,}", s):
            flush_list()
            out.append("<hr/>")
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush_list()
            lvl = min(len(m.group(1)), 3)
            _txt = m.group(2).strip()
            if _txt != "Table 1":          # 结构锚点，正式表题在下一行，避免重复
                out.append("<h%d>%s</h%d>" % (lvl, inline(_txt), lvl))
            i += 1
            continue

        # 表格：必须以「|…|」开头 **且下一行是分隔行**，否则只是正文里的竖线
        if _is_table_start(lines, i):
            flush_list()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            parsed = []
            for r in rows:
                cells = [c.strip() for c in re_split_row(r)]
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    continue                      # 分隔行
                parsed.append(cells)
            if parsed:
                out.append("<table>")
                for ri, cells in enumerate(parsed):
                    tag = "th" if ri == 0 else "td"
                    out.append("<tr>" + "".join("<%s>%s</%s>" % (tag, inline(c), tag)
                                                for c in cells) + "</tr>")
                out.append("</table>")
            continue

        # 引用
        if s.startswith(">"):
            flush_list()
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(buf)))
            continue

        # 无序列表
        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            listbuf.append(m.group(1))
            i += 1
            continue

        # 段落（合并连续非空行）
        flush_list()
        buf = []
        while i < n:
            t = lines[i].strip()
            if (not t or t.startswith(("#", ">", "---"))
                    or re.match(r"^[-*]\s+", t)
                    or _is_table_start(lines, i)):
                break
            buf.append(t)
            i += 1
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(buf)))
        else:
            # 兜底：避免死循环
            out.append("<p>%s</p>" % inline(s))
            i += 1

    flush_list()
    return "\n".join(out)


md = open(os.path.join(SRC, "Manuscript.md"), encoding="utf-8").read()
body = md_to_html(md)
html_doc = ("<html><head><meta charset='utf-8'><style>%s</style></head><body>%s</body></html>"
            % (CSS, body))
# MD→HTML→DOCX→PDF 的中间物（HTML / 两个 PowerShell 脚本）放系统临时目录，
# 不进投稿包 —— 包内只留投稿系统要的东西。
TMPD = tempfile.mkdtemp(prefix="pkg_build_")
html_path = os.path.join(TMPD, "_manuscript.html")
open(html_path, "w", encoding="utf-8").write(html_doc)
print("  [2] Manuscript.md → HTML（%.1f KB）" % (os.path.getsize(html_path) / 1024))


# ── Word 转换（两段：HTML→DOCX，压紧表格，DOCX→PDF）──────────
PS1 = r"""
param([string]$Html,[string]$Docx)
$ErrorActionPreference='Stop'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.Options.ConfirmConversions = $false
$w.Options.CheckGrammarAsYouType = $false
try {
    $d = $w.Documents.Open($Html, [ref]$false, [ref]$false)
    $d.PageSetup.PageWidth  = $w.CentimetersToPoints(21.0)
    $d.PageSetup.PageHeight = $w.CentimetersToPoints(29.7)
    $d.PageSetup.TopMargin    = $w.CentimetersToPoints(2.5)
    $d.PageSetup.BottomMargin = $w.CentimetersToPoints(2.5)
    $d.PageSetup.LeftMargin   = $w.CentimetersToPoints(2.5)
    $d.PageSetup.RightMargin  = $w.CentimetersToPoints(2.5)
    $d.Sections.Item(1).Footers.Item(1).PageNumbers.Add(2, $true) | Out-Null
    $d.SaveAs2($Docx, 16)
    $d.Close([ref]$false)
} finally {
    $w.Quit()
}
"""

PS2 = r"""
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
} finally {
    $w.Quit()
}
"""

docx_path = os.path.join(D["manu"], "Manuscript.docx")
pdf_path = os.path.join(D["manu"], "Manuscript.pdf")
ps1 = os.path.join(TMPD, "_conv1.ps1")
ps2 = os.path.join(TMPD, "_conv2.ps1")
open(ps1, "w", encoding="utf-8-sig").write(PS1)
open(ps2, "w", encoding="utf-8-sig").write(PS2)

r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1,
                    "-Html", html_path, "-Docx", docx_path],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("  [3] HTML→DOCX exit=%s" % r.returncode)
if r.returncode != 0:
    print("       stderr: %s" % (r.stderr or "")[:400])

# Word 的 HTML 导入会给表格单元格加段落间距，把表格撑得很高；转换后压紧
try:
    from docx import Document as _Docx
    from docx.shared import Pt as _Pt
    _d = _Docx(docx_path)
    for _t in _d.tables:
        for _row in _t.rows:
            for _c in _row.cells:
                for _p in _c.paragraphs:
                    _p.paragraph_format.space_before = _Pt(0)
                    _p.paragraph_format.space_after = _Pt(0)
                    _p.paragraph_format.line_spacing = 1.0
    _d.save(docx_path)
    print("  [3b] 表格已压紧（单元格间距 0 / 单倍行距）")
except Exception as e:
    print("  [3b] 表格压紧失败：%s" % e)

r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps2,
                    "-Docx", docx_path, "-Pdf", pdf_path],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("  [3c] DOCX→PDF exit=%s  %s" % (r.returncode, (r.stdout or "").strip()[:40]))
if r.returncode != 0:
    print("       stderr: %s" % (r.stderr or "")[:400])

# ── 复制稿件源 ────────────────────────────────────────────
shutil.rmtree(TMPD, ignore_errors=True)   # 清掉 HTML / PowerShell 中间件
shutil.copy2(os.path.join(SRC, "Manuscript.md"), os.path.join(D["manu"], "Manuscript_source.md"))

# ── 正文图 ────────────────────────────────────────────────
FG = os.path.join(B, "04_图表")
figmap = [("Fig1_两库筛选流程图", "Fig1"),
          ("Fig2_判别稳与校准漂", "Fig2"),
          ("Fig3_三评分校准漂移对比", "Fig3"),
          ("Fig4_规模分层与临床影响", "Fig4"),
          ("Fig5_重校准与收缩收益", "Fig5")]
nfig = 0
for stem, newname in figmap:
    for ext, dest in [(".png", D["figs"]), (".pdf", D["figp"])]:
        src = os.path.join(FG, stem + ext)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest, newname + ext))
            nfig += 1
print("  [4] 正文图 %d 个文件" % nfig)

# ── 补充材料 ──────────────────────────────────────────────
shutil.copy2(os.path.join(B, "Supplementary_Information.pdf"),
             os.path.join(D["supp"], "Supplementary_Information.pdf"))

# ── 报告清单 ──────────────────────────────────────────────
A = os.path.join(B, "07_投稿附件")
for f in ["STROBE_checklist_投稿版.docx", "STROBE_checklist_投稿版.pdf"]:
    src = os.path.join(A, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(D["chk"], f.replace("_投稿版", "")))

print("  [5] 补充材料 + 报告清单已归集")

# ── README ────────────────────────────────────────────────
def sz(p):
    return "%.0f KB" % (os.path.getsize(p) / 1024) if os.path.exists(p) else "缺失"


README = """# 投稿包 — Scientific Reports

**这一包是投稿时直接取文件的地方。** 不要在这里改内容；改 `08_正文/` 下的源文件，
然后重跑 `整理_投稿包.py` 重建本包。

重建命令（在工作目录 `09_路B_跨院校准/` 下）：

```
python -X utf8 整理_投稿包.py
```

---

## 上传顺序与对应文件

Sci Rep 投稿系统按下列槽位收文件。**主表不单独上传**（已嵌入稿件文件）。

| # | 系统槽位 | 本包文件 | 格式要求 | 大小 |
|---|---|---|---|---|
| 1 | Cover letter | `5_投稿信_Cover_Letter/` | .doc/.docx/.pdf，仅编辑可见 | 待写 |
| 2 | Manuscript File | `1_稿件_Manuscript/Manuscript.docx` | **只允许一个文件** | {m1} |
| 3 | Main Figure File(s) | `2_正文图_Main_Figures/` | .jpg/.eps/.tiff/.psd/.png/.pdf | {m2} |
| 4 | Main Table(s) | — | **不得单独上传**，已在稿件内 | — |
| 5 | Supplementary Information | `3_补充材料_Supplementary/Supplementary_Information.pdf` | 单独文件，优先单一 PDF | {m3} |
| 6 | Reporting checklist | `4_报告清单_Reporting_Checklist/STROBE_checklist.pdf` | 建议提交 | {m4} |

> 官方清单原文：*"Main Table(s) — Do not upload separately. Must be included in the Manuscript File."*
> 以及 *"Supplementary material is uploaded separately, and not included in the Manuscript File."*
> 两件事都已按此办理：主表在稿件内、补充材料独立成包。

---

## 每个文件夹里有什么

**`1_稿件_Manuscript/`**
- `Manuscript.docx` — **上传用**。可编辑，主表是真正的 Word 表格（非图片）。
- `Manuscript.pdf` — 校对用 / 备用上传格式。
- `Manuscript_source.md` — Markdown 源，仅供追溯。

**`2_正文图_Main_Figures/`**
- `Fig1.png … Fig5.png` — 600 dpi PNG（Sci Rep 官方清单明列接受 .png）。
- `PDF/Fig1.pdf … Fig5.pdf` — 矢量版，若编辑要求矢量则用这一套。

**`3_补充材料_Supplementary/`**
- `Supplementary_Information.pdf` — {s3pages} 页 / {m3}：封面目录 + 图 S1–S3 + 表 S1–S3 + Supplementary Note。
  正文型 PDF（文字可选中、可检索），表为真正的表格，每项各占一页。

**`4_报告清单_Reporting_Checklist/`**
- `STROBE_checklist.docx` — **可编辑，页码列留空待填**。
- `STROBE_checklist.pdf` — 填好后重新导出的版本。

**`5_投稿信_Cover_Letter/`** — 待写，需提供推荐/回避审稿人。

**`6_上传前自查/`** — 上传前逐项打勾；含待填占位符清单。

---

## 现在还不能上传，因为还差

1. **5 个占位符**（见 `6_上传前自查/待填占位符清单.md`）：一作姓名、通讯邮箱、CRediT
   逐位贡献、伦理委员会名称+批件号、Competing interests 声明。稿件里以**黄底 `⟨…⟩`** 标出，
   在 Word 里一眼可见。
2. **STROBE 清单的页码列** —— 等 `Manuscript.docx` 定稿后填。
3. **Cover letter**。
4. **灰度打印试读** 5 张正文图 + 3 张补充图。

---

## 一个容易踩的坑

本包的 `Manuscript.docx` 由 `Manuscript.md` **自动生成**。如果你直接在 Word 里改 DOCX，
下次重跑 `整理_投稿包.py` 会把改动**覆盖掉**。

正确做法：改 `08_正文/` 下的源文件（或 `装配_Manuscript.py`）→ 重跑装配 → 重跑本脚本。
"""

# 填入实际大小
_s3 = os.path.join(D["supp"], "Supplementary_Information.pdf")
try:
    import fitz as _fitz
    _s3p = _fitz.open(_s3).page_count
except Exception:
    _s3p = "?"

README = README.format(
    s3pages=_s3p,
    m1=sz(docx_path),
    m2="%d 个文件" % nfig,
    m3=sz(os.path.join(D["supp"], "Supplementary_Information.pdf")),
    m4=sz(os.path.join(D["chk"], "STROBE_checklist.pdf")),
)
open(os.path.join(PKG, "README_上传说明.md"), "w", encoding="utf-8").write(README)

# ── 待填占位符清单 ────────────────────────────────────────
man = open(os.path.join(SRC, "Manuscript.md"), encoding="utf-8").read()
ph = re.findall(r"⟨[^⟩]*⟩", man)
seen, uniq = set(), []
for p in ph:
    if p not in seen:
        seen.add(p)
        uniq.append(p)

PH = "# 待填占位符清单\n\n"
PH += "稿件中共 **%d 处**黄底 `⟨…⟩` 占位符（去重后 %d 类）。\n\n" % (len(ph), len(uniq))
PH += "在 `Manuscript.docx` 里用 Word 的查找功能搜 `⟨` 即可逐个定位。\n\n"
PH += "| # | 占位符原文 | 出现次数 | 要填什么 |\n|---|---|---|---|\n"
hints = {
    "⟨第一作者": "第一作者姓名 + 拼音（投稿系统须一致）",
    "⟨通讯": "通讯作者邮箱（须与系统一致）",
    "⟨逐位作者": "逐位作者、逐项 CRediT 贡献",
    "⟨ETHICS": "伦理委员会全称 + 批件号（或免审判定）",
    "⟨Data": "已由本流程填好 Data Availability，如仍出现则需核对",
    "⟨Competing": "每位作者的利益冲突声明（无则写 declare no competing interests）",
}
for k, v in enumerate(uniq, 1):
    hint = next((h for key, h in hints.items() if v.startswith(key)), "见上下文")
    PH += "| %d | `%s` | %d | %s |\n" % (k, v[:70], ph.count(v), hint)
PH += """
---

## 已由流程代填、无需你处理的

- **Data Availability** —— 已写成正式英文段落，置于 References **之前**（Sci Rep 强制位置），
  含 Zenodo DOI 与代码库地址。
- **Funding** —— `This research received no external funding.`（STROBE 第 22 条要求必须写入稿件）。
"""
open(os.path.join(D["self"], "待填占位符清单.md"), "w", encoding="utf-8").write(PH)

# ── 上传前自查清单 ────────────────────────────────────────
SC = """# 上传前自查清单

## A. 官方硬性要求（不合规会被退回、不进评审）

| # | 检查项 | 依据 | 状态 |
|---|---|---|---|
| 1 | 稿件**只有一份文件** | 官方清单 "Only one file permitted" | ☐ |
| 2 | 主表**在稿件内**、可编辑、非图片 | "Do not upload separately" | ☐ |
| 3 | 稿件内**无脚注**、**无修订痕迹** | "No footnotes" / "Tracked changes must not be used" | ☐ |
| 4 | 标题与投稿系统**完全一致** | "Exactly matches the title entered on the submission system" | ☐ |
| 5 | 摘要与系统**完全一致**，无引用、无小标题 | "Does not contain citations… not a structured abstract" | ☐ |
| 6 | 通讯作者带 **\\*** 且**邮箱在标题页** | "Email address(es) … should be provided on the title page" | ☐ |
| 7 | 每位作者均有**单位 + 国别**、上标编号 | "Affiliations (including country)" | ☐ |
| 8 | **Author contributions** 每位作者都列出 | "every author's contribution must be listed" | ☐ |
| 9 | **Competing interests** 在 `Additional Information` 下 | "under the heading 'Additional Information'" | ☐ |
| 10 | **Data Availability** 在 **References 之前** | "at the end of the main text, before the 'References' section" | ☐ |
| 11 | 每张正文图表都有**图注**，置于 References 之后 | "These should be placed at the end of the manuscript, after the references" | ☐ |
| 12 | 补充图表图注**不**出现在稿件内 | "Only legends for main display items should be included in the Manuscript File" | ☐ |
| 13 | 正文图 ≤ **8** 个 display items | 本稿 5 图 + 1 表 = 6（Fig.5 合并后有余量） | ☑ |
| 14 | 摘要 ≤ **200** 词 | 自动质检 200/200 | ☑ |
| 15 | 标题 ≤ **20** 词 | 自动质检通过 | ☑ |
| 16 | 正文（Intro+Results+Discussion）≤ **4,500** 词 | 自动质检通过 | ☑ |

## B. 图表格式

| # | 检查项 | 状态 |
|---|---|---|
| 17 | 5 张正文图为 **600 dpi**、宽 ≥ 89 mm（单栏）/ 183 mm（双栏） | ☐ |
| 18 | 图内**无主标题、无解释性副标题、无底部注释** | ☑ |
| 19 | **灰度打印试读**：10 张图在黑白下仍可区分 | ☐ **只有作者能做** |
| 20 | 图中文字在 100% 打印尺寸下 ≥ 5 pt | ☐ |

## C. 内容层面

| # | 检查项 | 状态 |
|---|---|---|
| 21 | 5 个 `⟨…⟩` 占位符全部填完 | ☐ |
| 22 | STROBE 清单页码列已填 | ☐ |
| 23 | Cover letter 已写、含推荐/回避审稿人 | ☐ |
| 24 | 三条措辞红线未违反（残余变异≠医疗质量 / MIMIC≠多中心外部验证 / EB 非临床推荐） | ☑ 自动检查通过 |
| 25 | 参考文献 22 条全部在正文中被引用、编号连续 | ☑ |

## D. 上传后

| # | 检查项 | 状态 |
|---|---|---|
| 26 | 系统内作者顺序、单位、通讯与稿件一致 | ☐ |
| 27 | 系统内摘要粘贴后无格式丢失 | ☐ |
| 28 | ORCID 已关联 | ☐ |
| 29 | Data Availability / Competing interests 在系统中与稿件一致 | ☐ |
"""
open(os.path.join(D["self"], "上传前自查清单.md"), "w", encoding="utf-8").write(SC)

# ── Cover letter 占位 ─────────────────────────────────────
CL = """# Cover letter（待写）

写好之后放在这个文件夹，文件名 `Cover_letter.docx` 或 `.pdf`。

---

## 起草前需要你提供

1. **推荐审稿人 3–5 位**（姓名、单位、邮箱；须与本文无利益关系、近 5 年有相关发表）
2. **需回避的审稿人**（如有；建议写明理由，如直接竞争或存在分歧）
3. 是否同意 **transparent peer review**（Sci Rep 会公开审稿记录，可选）
4. 是否有**预印本**（若有，需在 cover letter 中声明，避免重复发表质疑）

---

## 已确定、可直接写进信里的要点

- 期刊：Scientific Reports（Article）
- 无基金资助
- 未一稿多投；全部作者已阅读并同意投稿
- 数据与代码已归档：https://doi.org/10.5281/zenodo.23479141
- 报告指南：STROBE + RECORD，清单已随稿提交
- 三条必须守住的分寸（**写信时也不能越界**）：
  1. 残余院间变异**不归因于**医疗质量
  2. MIMIC-IV 只验证**收缩参数跨库迁移**，不是"外部多中心验证"
  3. 经验贝叶斯收缩是**统计学建议**，不是临床推荐
"""
open(os.path.join(D["cl"], "待填说明.md"), "w", encoding="utf-8").write(CL)

print("  [6] README / 自查清单 / 待填清单 / Cover letter 说明 已生成")
print("\n  ✔ 投稿包：%s" % PKG)
for k, d in D.items():
    files = sorted(os.listdir(d))
    print("     %-34s %d 项" % (os.path.relpath(d, PKG), len(files)))
