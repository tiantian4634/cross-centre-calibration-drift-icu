# -*- coding: utf-8 -*-
"""组装 Supplementary Information 单文件 PDF。

Sci Rep 要求：
  · 单独上传、优先单文件 PDF、≤50 MB
  · 图/表须编号为 Supplementary Fig. S1 / Table S1，与正文编号分开
  · Supplementary Note **不编号**（标题可选），故本稿改称「Supplementary Note」+ 标题
  · 每张图/表须在文件内自带简短标题与图注
"""
import io, sys, os, re, glob
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
FG = os.path.join(B, "04_图表")
OUT_PDF = os.path.join(B, "Supplementary_Information.pdf")

DPI = 190
W, H = int(8.27 * DPI), int(11.69 * DPI)          # A4 竖版
ML, MR, MT, MB = int(0.85 * DPI), int(0.85 * DPI), int(0.75 * DPI), int(0.75 * DPI)
CW = W - ML - MR

FN = r"C:\Windows\Fonts\msyh.ttc"
FNB = r"C:\Windows\Fonts\msyhbd.ttc"
F_TITLE = ImageFont.truetype(FNB, int(0.20 * DPI))
F_H = ImageFont.truetype(FNB, int(0.145 * DPI))
F_B = ImageFont.truetype(FN, int(0.112 * DPI))
F_S = ImageFont.truetype(FN, int(0.098 * DPI))
LH_B, LH_S = int(0.168 * DPI), int(0.147 * DPI)

PAGES = []


def newpage():
    im = Image.new("RGB", (W, H), "white")
    PAGES.append(im)
    return im, ImageDraw.Draw(im)


def wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) <= width:
                line = t
            else:
                if line:
                    out.append(line)
                line = w
        if line:
            out.append(line)
    return out


def block(d, y, text, font, lh, width=CW, x=ML, fill="#111111"):
    for ln in wrap(d, text, font, width):
        if ln:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ── 1. 封面 ──────────────────────────────────────────────
im, d = newpage()
y = MT
y = block(d, y, "Supplementary Information", F_TITLE, int(LH_B * 1.25)); y += int(0.28 * DPI)
y = block(d, y, "Discrimination transports, calibration does not: calibration drift in severity "
                "scoring across 187 intensive-care units", F_B, LH_B); y += int(0.30 * DPI)
CONT = """Contents

  Supplementary Fig. S1    Case-mix ladder: between-centre heterogeneity across nested models
  Supplementary Fig. S2    Position of the single-centre MIMIC-IV cohort within the eICU-CRD distribution
  Supplementary Fig. S3    Year-to-year stability of the calibration offset within hospitals
  Supplementary Table S1   Cohort characteristics
  Supplementary Table S2   Between-centre variance estimated under four frameworks
  Supplementary Note       Prespecified analysis plans: index, chronology and disclosures

Note on numbering. Supplementary figures and tables are numbered S1, S2 … separately from the
main article. Supplementary Notes are not numbered, in accordance with the journal's
supplementary material policy."""
y = block(d, y, CONT, F_B, LH_B); y += int(0.28 * DPI)
y = block(d, y, "The analysis plans reproduced in the Supplementary Note were written before the\n"
                "corresponding analyses were executed. Their file timestamps, an explicit disclosure of\n"
                "one timestamp defect, and a post-hoc correction to the weighting of the shrinkage target\n"
                "are all included, so that the reader can verify what was specified before what was run.",
          F_S, LH_S, fill="#333333")

# ── 2. 三张补充图 ────────────────────────────────────────
LEG = open(os.path.join(B, "图注_legend.md"), encoding="utf-8").read()
blocks = re.split(r"\n# ", LEG)
LEGS = {}
for blk in blocks:
    head = blk.split("\n")[0].strip()
    m = re.match(r"^Supplementary Fig\. S(\d+)$", head)
    if not m:
        continue
    eng = re.search(r"### English legend\s*\n(.*?)(?:\n### |\Z)", blk, re.S)
    if not eng:
        continue
    LEGS["S" + m.group(1)] = re.sub(r"^>\s?", "", eng.group(1), flags=re.M).strip()

TITLES = {
    "S1": "Supplementary Figure S1. Case-mix ladder: between-centre heterogeneity across nested models.",
    "S2": "Supplementary Figure S2. Position of the single-centre MIMIC-IV cohort within the eICU-CRD distribution of calibration offsets.",
    "S3": "Supplementary Figure S3. Year-to-year stability of the calibration offset within hospitals.",
}
FILES = {"S1": "SuppFigS1_病例组合阶梯.png",
         "S2": "SuppFigS2_MIMIC在多中心分布中的位置.png",
         "S3": "SuppFigS3_同一中心两年校准偏移的稳定性.png"}

for k in ["S1", "S2", "S3"]:
    im, d = newpage()
    y = MT
    y = block(d, y, TITLES[k], F_H, int(LH_B * 1.2)); y += int(0.14 * DPI)
    fp = os.path.join(FG, FILES[k])
    with Image.open(fp) as fig_im:
        fig_im = fig_im.convert("RGB")
        sc = min(CW / fig_im.width, int(H * 0.62) / fig_im.height)
        nw, nh = int(fig_im.width * sc), int(fig_im.height * sc)
        im.paste(fig_im.resize((nw, nh), Image.LANCZOS), (ML + (CW - nw) // 2, y))
        y += nh + int(0.20 * DPI)
    block(d, y, LEGS.get(k, "(legend missing)"), F_S, LH_S, fill="#222222")
print("  [1] 三张补充图已入册")

# ── 3. 两张补充表 ────────────────────────────────────────
tab = open(os.path.join(B, "08_正文", "Tables_表格.md"), encoding="utf-8").read()


def md_table(txt, name):
    """按「连续管道行块」定位表格，避免被表前的粗体标题截断。"""
    i = txt.find(name)
    if i < 0:
        return None, None
    ls = txt[i:].split("\n")
    start = None
    for k, l in enumerate(ls):
        if l.strip().startswith("|"):
            start = k
            break
    if start is None:
        return None, None
    end = start
    while end < len(ls) and ls[end].strip().startswith("|"):
        end += 1
    lines = ls[start:end]
    seg = "\n".join(ls[:end])
    return lines, seg


for fname, label in [("## Supplementary Table S1", "Supplementary Table S1. Cohort characteristics."),
                     ("## Supplementary Table S2", "Supplementary Table S2. Between-centre variance estimated under four frameworks.")]:
    lines, seg = md_table(tab, fname)
    if not lines:
        print("  ✘ 未找到 %s" % fname)
        continue
    rows = [[c.strip().replace("**", "") for c in l.strip().strip("|").split("|")] for l in lines]
    rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
    im, d = newpage()
    y = MT
    y = block(d, y, label, F_H, int(LH_B * 1.2)); y += int(0.18 * DPI)
    ncol = max(len(r) for r in rows)
    colw = [0] * ncol
    for r in rows:
        for i, c in enumerate(r):
            colw[i] = max(colw[i], int(d.textlength(c, font=F_S)) + int(0.10 * DPI))
    tot = sum(colw)
    if tot > CW:                                   # 超宽则等比压缩
        k = CW / tot
        colw = [int(c * k) for c in colw]
        tot = CW
    for ri, r in enumerate(rows):
        x = ML
        is_head = ri == 0
        if is_head:
            d.rectangle([ML, y - int(0.03 * DPI), ML + tot, y + LH_S + int(0.05 * DPI)],
                        fill="#EFF3F6")
        for i, c in enumerate(r):
            d.text((x, y), c, font=F_S, fill="#111111")
            x += colw[i]
        y += LH_S + (int(0.05 * DPI) if is_head else 0)
        d.line([ML, y - int(0.03 * DPI), ML + tot, y - int(0.03 * DPI)], fill="#8A97A3", width=1)
    y += int(0.28 * DPI)
    lm = re.search(r"\*\*Supplementary Table S\d+ legend\.\*\*\s*(.*?)(?=\n\n>|\n\n\*\*|\n## |\Z)",
                   tab[tab.find(fname):], re.S)
    if lm:
        block(d, y, "Legend. " + re.sub(r"\s+", " ", lm.group(1)).strip(), F_S, LH_S, fill="#333333")
    else:
        block(d, y, "(legend missing)", F_S, LH_S, fill="#8B0000")
print("  [2] 两张补充表已入册")

# ── 4. Supplementary Note ────────────────────────────────
note = open(os.path.join(B, "07_投稿附件", "S1_分析计划汇总与披露.md"), encoding="utf-8").read()
note = re.sub(r"^# .*?\n", "", note, count=1)      # 去掉原一级标题
im, d = newpage()
y = MT
y = block(d, y, "Supplementary Note", F_H, int(LH_B * 1.2))
y = block(d, y, "Prespecified analysis plans: index, chronology and disclosures", F_B, LH_B, fill="#333333")
y += int(0.20 * DPI)
for ln in note.split("\n"):
    ln = ln.strip()
    if not ln:
        y += int(0.09 * DPI)
        continue
    if ln.startswith("|"):
        ln = re.sub(r"\s*\|\s*", "   ", ln.strip("|")).replace("**", "")
        f, lh, fill = F_S, LH_S, "#222222"
    elif ln.startswith(("#", "##", "###")):
        ln = re.sub(r"^#+\s*", "", ln).replace("**", "")
        f, lh, fill = F_B, int(LH_B * 1.1), "#000000"
        y += int(0.08 * DPI)
    else:
        ln = ln.replace("**", "").replace("`", "")
        f, lh, fill = F_S, LH_S, "#111111"
    if y + lh > H - MB:
        im, d = newpage()
        y = MT
    y = block(d, y, ln, f, lh, fill=fill)
print("  [3] Supplementary Note 已入册")

# ── 5. 输出 ─────────────────────────────────────────────
tmp = os.path.join(B, "_si_tmp.pdf")
PAGES[0].save(tmp, "PDF", save_all=True, append_images=PAGES[1:], resolution=DPI)
os.replace(tmp, OUT_PDF)
sz = os.path.getsize(OUT_PDF)
print("\n  ✔ %s" % os.path.basename(OUT_PDF))
print("    页数 %d ｜ %.1f MB  %s" % (len(PAGES), sz / 1048576,
                                      "✔ ≤50 MB" if sz <= 50 * 1048576 else "✘ 超 50 MB"))
r = PdfReader(OUT_PDF)
print("    pypdf 复核页数 %d" % len(r.pages))
print("=" * 90)