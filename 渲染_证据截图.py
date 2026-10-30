# -*- coding: utf-8 -*-
"""渲染 v3 预审修订版 PDF 的争议页为 PNG（M2/M3/M4/M10/refs 的页面级证据）。"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import fitz

SRC = r"10_预审版\正文初稿_v3_预审修订版.pdf"
OUTDIR = r"10_预审版\_证据截图"
os.makedirs(OUTDIR, exist_ok=True)

doc = fitz.open(SRC)
targets = {
    "fig1_legend_193367.png": "protected139",
    "table1_page.png": "Table 1. Between-centre variation",
    "fig2_page.png": "Discrimination transports across centres",
    "slope_formula_page.png": "logit(y)",
    "refs_page.png": "Johnson, A. E. W., Kramer",
    "legend_fig1_flow.png": "Flow of participants",
}
found = {}
for i, page in enumerate(doc):
    text = page.get_text()
    for fn, needle in targets.items():
        if needle in text and fn not in found:
            found[fn] = i
for fn, pno in found.items():
    page = doc[pno]
    pix = page.get_pixmap(dpi=140)
    out = os.path.join(OUTDIR, fn)
    pix.save(out)
    print(f"{fn}: 第 {pno + 1} 页 -> {out}")
print("渲染页数:", len(found), "/", len(targets))
