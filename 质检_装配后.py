# -*- coding: utf-8 -*-
"""装配后质检：图注/引用/段落顺序/占位符/Sci Rep 结构要求。"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准\08_正文\Manuscript.md"
t = open(P, encoding="utf-8").read()
ls = t.split("\n")
ok = True

def chk(cond, msg):
    global ok
    ok &= bool(cond)
    print("    %s %s" % ("✔" if cond else "✘", msg))

print("=" * 84)
print("  装配质检")
print("=" * 84)

print("\n[1] 段落顺序（Sci Rep 规定）")
order = ["# Title Page", "# Abstract", "## Introduction", "## Results", "## Discussion",
         "## Study design and setting", "## References", "## Author contributions",
         "## Data Availability", "## Additional Information", "## Figure legends", "## Table 1"]
pos = []
for o in order:
    if t.startswith(o):                     # Title Page 是全文第一行
        i = 0
    else:
        i = t.find("\n" + o + "\n")
        if i < 0:
            i = t.find("\n" + o)
    pos.append((o, i))
prev = -1
for o, i in pos:
    good = i >= 0 and i > prev
    chk(good, "%-32s 位置 %6d %s" % (o, i, "" if good else "顺序错误"))
    if good:
        prev = i

print("\n[2] 图注与正文图引用一致性")
legs = re.findall(r"^\*\*Figure (\d+)\*\*", t, re.M)
refs = re.findall(r"\(Fig(?:ure)?\.?\s*(\d+)", t) + re.findall(r"Fig\. (\d+)", t)
legs_s, refs_s = sorted(set(map(int, legs))), sorted(set(map(int, refs)))
print("      图注: %s" % legs_s)
print("      正文引用: %s" % refs_s)
missing = [r for r in refs_s if r not in legs_s]
extra = [l for l in legs_s if l not in refs_s]
chk(not missing, "正文引用但无图注: %s" % (missing or "无"))
chk(not extra, "有图注但正文未引用: %s" % (extra or "无"))

print("\n[3] 补充材料引用")
supp = sorted(set(re.findall(r"Supplementary (?:Fig(?:ure)?\.?\s*S?\d+|Table\s*S\d+|Note\s*S\d+)", t)))
for s in supp:
    print("      " + s)
chk(len(supp) >= 3, "补充材料引用数 ≥3（现 %d）" % len(supp))

print("\n[4] 参考文献")
r0 = t.find("## References")
r1 = t.find("## Author contributions")
refs_list = re.findall(r"(?m)^\[(\d+)\]", t[r0:r1]) if r0 > 0 else []
print("      列表条数: %d（第 1–%s 条）" % (len(refs_list), refs_list[-1] if refs_list else "—"))
cited = sorted({int(x) for c in re.findall(r"\[(\d+(?:,\s*\d+)*)\]", t[:r0])
                for x in re.split(r",\s*", c)})
uncited = [n for n in range(1, len(refs_list) + 1) if n not in cited]
print("      正文已引用: %s" % cited)
chk(not uncited, "列表中未被引用的条目: %s" % (uncited if uncited else "无"))
chk(len(refs_list) <= 60, "参考文献 ≤60（现 %d）" % len(refs_list))

print("\n[5] 占位符（须作者填写，此处仅确认存在）")
for tok in ["⟨First Author", "⟨EMAIL⟩", "⟨逐位作者", "⟨ETHICS⟩", "⟨Data Availability"]:
    print("      %-24s %s" % (tok, "✔" if tok in t else "✘ 缺"))

print("\n[6] Sci Rep 结构要求")
chk("## Results" in t and t.count("### ") >= 8, "Results 含小标题（%d 个）" % len(re.findall(r"^### ", t, re.M)))
d_sec = t.find("## Discussion"); r_sec = t.find("## References")
disc = t[d_sec:r_sec] if d_sec > 0 and r_sec > d_sec else ""
chk(not re.search(r"^### ", disc, re.M), "Discussion 无小标题 ✔")
chk("**Keywords.**" in t, "含 Keywords 行")
kw = re.search(r"\*\*Keywords\.\*\*\s*(.+)", t)
if kw:
    kws = [k.strip() for k in kw.group(1).split("·")]
    chk(len(kws) <= 6, "关键词 ≤6（现 %d）" % len(kws))
chk("footnote" not in t.lower(), "无脚注")
chk("This research received no external funding" in t, "Funding 声明存在")

print("\n[7] 三条措辞红线（正文）")
chk(not re.search(r"quality of care|医疗质量|质量差异", t), "无医疗质量归因")
neg = len(re.findall(r"not multicentre external validation", t))
chk(neg >= 1, "「非外部多中心验证」为否定表述（%d 处）" % neg)
chk("not a clinical recommendation" in t, "结论含「非临床推荐」")

print("\n[8] 摘要")
m = re.search(r"# Abstract\n\n(.*?)\n\n\*\*Keywords", t, re.S)
ab = re.sub(r"[*_`]+", "", m.group(1)).replace("\n", " ")
w = [x for x in re.findall(r"\S+", ab) if re.search(r"[A-Za-z0-9]", x)]
print("      词数 %d / 200" % len(w))
chk(len(w) <= 200, "摘要 ≤200 词")
chk(not re.search(r"^\*\*(Background|Methods|Results|Conclusions)\.", ab, re.M), "摘要非结构化")

print("\n" + "=" * 84)
print("  %s" % ("✔ 全部通过" if ok else "✘ 有未通过项，见上"))
print("=" * 84)
print("  文件: %s  (%.1f KB / %d 行)"
      % (os.path.basename(P), os.path.getsize(P) / 1024, len(ls)))