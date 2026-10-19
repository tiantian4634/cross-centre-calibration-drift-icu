import re, io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
# 可能承载结论的数值型字面量（百分比、四位小数、AUC、I² 等）
NUM = re.compile(r"(?<![\w.])\d{1,3}\.\d{1,2}\s*%|\b0\.\d{3,4}\b|\b\d{1,3}\.\d\s*pp\b")
# 标注类调用
ANN = re.compile(r"\.(annotate|text|axhline)\s*\(|ax\.text\s*\(|fig\.text\s*\(")

print("=" * 84)
print("  图脚本标注硬编码扫描")
print("=" * 84)

for f in sorted(glob.glob(os.path.join(B, "figures_*.py")) + glob.glob(os.path.join(B, "figure1_*.py"))):
    name = os.path.basename(f)
    lines = open(f, encoding="utf-8").read().split("\n")
    hits = []
    for i, ln in enumerate(lines, 1):
        if ANN.search(ln) or (hits and lines[i - 2].strip().startswith(("xy=", "ax.annotate"))):
            m = NUM.search(ln)
            if m:
                hits.append((i, ln.strip()))
    print("\n  ── %s" % name)
    if hits:
        for i, ln in hits:
            print("    行 %-4d %s" % (i, ln[:110]))
    else:
        print("    ✔ 无数值硬编码")

print("\n" + "=" * 84)
print("  备注：数据驱动的 f-string（如 f'{M[\"abar_eicu\"]:+.3f}'）不计为硬编码")
print("=" * 84)