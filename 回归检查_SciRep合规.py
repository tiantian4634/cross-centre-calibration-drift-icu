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
    if not re.match(r"图\s*\d", b) and "图1" not in b[:6]:
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
for nm, txt in [("Methods", MET), ("Abstract", ABS)]:
    for mt in re.finditer(r"(?<![\d,.])(\d{5,})(?![\d,])", re.sub(r"[\d,]", lambda m: m.group(0), txt)):
        pass
    for ln in txt.split("\n"):
        for mt in re.finditer(r"(?<![\d,.])(\d{5,})(?![\d,.])", ln):
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
print("\n[7] Display items（上限 8 = 图+表合计）")
import glob
pngs = glob.glob(os.path.join(R, "04_图表", "*.png"))
print("    现有主图      %d 张  %s" % (len(pngs), "✘ 超限" if len(pngs) > 8 else "✔"))
print("    加上 3 张表   = %d    %s" % (len(pngs) + 3, "✘ 需砍到 8" if len(pngs) + 3 > 8 else "✔"))

print("\n" + "=" * 88)