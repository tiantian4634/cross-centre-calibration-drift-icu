# -*- coding: utf-8 -*-
"""Sci Rep 投稿合规自动核对（可机器判定的部分）。"""
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
def rd(p):
    fp = os.path.join(R, p)
    return open(fp, encoding="utf-8").read() if os.path.exists(fp) else None

ABS = rd(r"08_正文\Abstract_摘要_SciRep版.md") or ""
MET = rd(r"08_正文\Methods.md") or ""
LEG = rd(r"图注_legend.md") or ""

print("=" * 88)
print("  Sci Rep 投稿合规 · 自动核对")
print("=" * 88)

def words(t):
    return [w for w in re.findall(r"\S+", re.sub(r"\*+", "", t)) if re.search(r"[A-Za-z0-9]", w)]

# ---------- 1. 摘要 ----------
print("\n[1] ABSTRACT（官方要求：≤200 词 / 非结构化 / 不含引用 / 无子标题）")
m = re.search(r"## 摘要（英文投稿版）\n(.*?)\n---", ABS, re.S)
body = re.sub(r"\*+", "", m.group(1)).replace("\n", " ") if m else ""
n = len(words(body))
print("    词数           %-4d / 200   %s" % (n, "✔" if n <= 200 else "✘ 超限"))
subh = re.findall(r"^\*\*[^*]+\.\*\*|\n\s*(Background|Methods|Results|Conclusions)\.", body)
print("    小标题         %s  %s" % (subh or "无", "✔" if not subh else "✘"))
cit = re.findall(r"\[\d+\]|\d+\.\s+[A-Z][a-z]+,", body)
print("    内含引用       %s  %s" % (cit or "无", "✔" if not cit else "✘"))

# ---------- 2. 标题 ----------
print("\n[2] TITLE（官方要求：≤20 词 / 单句 / 无双关）")
for t in ["Discrimination transports, calibration does not: calibration drift in severity scoring across 187 intensive-care units",
          "Between-centre calibration drift in severity scoring and the local sample size needed to recalibrate"]:
    c = len(words(t))
    print("    %2d 词  %s  %s" % (c, "✔" if c <= 20 else "✘", t[:78]))

# ---------- 3. 关键词 ----------
print("\n[3] KEYWORDS（≤6）")
km = re.search(r"\*\*Keywords.*?\*\*\s*(.+)", ABS, re.S)
kw = re.findall(r"[A-Z][a-z\- ]{2,}", km.group(1).split("\n\n")[0]) if km else []
print("    提取到 %d 个  %s" % (len(kw), "✔" if len(kw) <= 6 else "✘"))
print("    " + (km.group(1).strip().replace("\n", " ")[:120] if km else "未找到"))

# ---------- 4. 图注 ----------
print("\n[4] FIGURE LEGENDS（每条 ≤350 词；须置于正文末参考文献之后）")
blocks = re.split(r"\n# ", LEG)
cnt = 0
for b in blocks:
    # 图注文件已统一为投稿编号（Figure N），补充图为 Supplementary Fig. SN
    if not re.match(r"Figure\s*\d", b):
        continue
    title = b.split("\n")[0].strip()
    eng = re.search(r"### English legend\s*\n(.*?)(?:\n### |\Z)", b, re.S)
    if eng:
        c = len(words(re.sub(r"^>\s?", "", eng.group(1), flags=re.M).replace("\n", " ")))
        cnt += 1
        print("    %-46s %4d 词  %s" % (title[:44], c, "✔" if c <= 350 else "✘ 超限"))
if cnt == 0:
    print("    ✘ 未能解析图注块（结构与预期不符，需人工确认）")

# ---------- 5. 千分位（官方：≥5 位数字须用逗号分隔）----------
print("\n[5] 千分位分隔（5 位及以上数字须用逗号；官方 style）")
bad = []
# 随机种子等「标识符」不是数量，按官方 style 不应加千分位
IDENT = {"20261019"}
for nm, txt in [("Methods", MET), ("Abstract", ABS)]:
    for ln in txt.split("\n"):
        for mt in re.finditer(r"(?<![\d,.])(\d{5,})(?![\d,.])", ln):
            if mt.group(1) in IDENT:
                continue
            bad.append((nm, mt.group(1), ln.strip()[:80]))
if bad:
    for nm, v, ln in bad[:8]:
        print("    ✘ %s 未加分隔: %-10s | %s" % (nm, v, ln))
else:
    print("    ✔ 未发现 5 位以上无分隔数字")

# ---------- 6. Methods 必含段落 ----------
print("\n[6] METHODS 与文末必备段落")
REQ = {
    "LLM 使用声明": "## Use of a large language model",
    "伦理声明（占位）": "## Ethics",
    "STROBE 声明": "## Reporting guidelines",
    "Software/seed": "## Software, seed and reproducibility",
    "分析层级（确认性/描述性）": "## Analysis framework and inferential status",
    "统计报告规则": "## Statistical reporting",
}
for k, v in REQ.items():
    print("    %s %-34s %s" % ("✔" if v in MET else "✘ 缺", k, ""))

STA = {"Data Availability": "Data Availability", "Author contributions": "Author contributions",
       "Competing interests / Additional Information": "Competing interests",
       "参考文献 Nature 格式": None, "图表在正文之后（legend after references）": None}
print("    —— 稿件尚缺的必备段落（结果/引言完成后才能定稿）——")
for k in ["Data Availability 独立小节（标题须为 'Data Availability'，置于 References 之前）",
          "Author contributions（置于 References 之后，逐位作者）",
          "Additional Information（Competing interests，与投稿系统一致）",
          "参考文献（编号列表 + 方括号文内引用）",
          "图注置于正文末、References 之后",
          "标题页（通讯作者 * 标注 + 邮箱 + 单位带上标与国家）",
          "Cover letter"]:
    print("    ⬜ " + k)

# ---------- 7. 已知阻塞 ----------
print("\n[7] Display items（上限 8 = 正文图+表合计；补充材料另计，不占额度）")
import glob
main_png = sorted(glob.glob(os.path.join(R, "04_图表", "Fig*.png")))
supp_png = sorted(glob.glob(os.path.join(R, "04_图表", "SuppFig*.png")))

# 正文表格数**实测**（此前硬编码为 1，会漏掉正文里的未编号表格，导致低估）
man_txt = open(os.path.join(R, "08_正文", "Manuscript.md"), encoding="utf-8").read()
_mlines = man_txt.split("\n")


def _is_sep(t):
    t = t.strip()
    if not t.startswith("|"):
        return False
    cells = [c.strip() for c in t.strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


main_tables = 0
for _i in range(len(_mlines) - 1):
    if _mlines[_i].strip().startswith("|") and _is_sep(_mlines[_i + 1]):
        if _i == 0 or not (_mlines[_i - 1].strip().startswith("|") and _is_sep(_mlines[_i])):
            main_tables += 1

NSUPP = len([1 for f in os.listdir(os.path.join(R, "08_正文"))
             if f == "Tables_表格.md"]) and 3   # SuppTable S1/S2/S3 在补充
NMAIN = main_tables
print("    正文主图      %d 张" % len(main_png))
print("    正文主表      %d 张  %s" % (NMAIN, "✔" if NMAIN <= 2 else "⚠ 请复核是否编号"))
print("    display items %d    %s" % (len(main_png) + NMAIN,
                                      "✘ 超限" if len(main_png) + NMAIN > 8 else "✔ 合规（上限 8）"))
print("    补充材料      图 %d 张 + 表 %d 张（不计入）" % (len(supp_png), NSUPP))

print("\n" + "=" * 88)