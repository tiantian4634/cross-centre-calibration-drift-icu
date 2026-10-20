# -*- coding: utf-8 -*-
"""核验 STROBE 清单引文，并精确定位首个分歧字符。"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
M = open(os.path.join(B, "08_正文", "Manuscript.md"), encoding="utf-8").read()
EXTRA = ""
for f in ["08_正文/Tables_表格.md", "图注_legend.md", "08_正文/BackMatter_文末段落.md"]:
    fp = os.path.join(B, f)
    if os.path.exists(fp):
        EXTRA += open(fp, encoding="utf-8").read()


CITE = re.compile(r"\[\d+(?:\s*[,\u2013-]\s*\d+)*\]")


def norm(s, strip_md=False):
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    if strip_md:                      # 正文里的 Markdown 强调标记与引用标记不属于稿件文字
        s = re.sub(r"\*+", "", s)
        s = s.replace("`", "")
        s = CITE.sub("", s)           # 只剥离 [20] / [1,2]，不误伤 [\u221212, 12]
    return re.sub(r"\s+", " ", s).strip()


NM = norm(M, True) + "  ###  " + norm(EXTRA, True)

S = open(os.path.join(B, "07_投稿附件", "STROBE_checklist_投稿版.md"), encoding="utf-8").read()
quotes = []
for line in S.split("\n"):
    if not line.startswith("| **"):
        continue
    item = re.match(r"\| \*\*([^*]+)\*\*", line).group(1)
    for q in re.findall(r"\u201c(.+?)\u201d", line):
        quotes.append((item, q))

ok, bad = 0, []
for item, q in quotes:
    segs = [s for s in re.split(r"\u2026", q) if len(norm(s)) >= 25] or [q]
    for s in segs:
        ns = CITE.sub("", norm(s)).strip()
        if ns in NM:
            ok += 1
            continue
        # 找最长可用前缀（≥25 字符）定位
        start = -1
        for k in range(len(ns), 24, -1):
            i = NM.find(ns[:k])
            if i >= 0:
                start, pref = i, k
                break
        if start < 0:
            bad.append((item, ns, None, None, None))
            continue
        # 从前缀处逐字符比较
        d = pref
        while d < len(ns) and NM[start + d] == ns[d]:
            d += 1
        bad.append((item, ns, d,
                    ns[max(0, d - 45):d + 55],
                    NM[start + max(0, d - 45):start + d + 55]))

print("  引文片段 %d 条 ｜ ✔ %d ｜ ✘ %d\n" % (ok + len(bad), ok, len(bad)))
for item, ns, d, mine, theirs in bad:
    print("  ── [%s] ──" % item)
    if d is None:
        print("     完全无法定位（可能非正文引文）")
        print("     引文：%s" % ns[:130])
    else:
        print("     第 %d 字符处分歧" % d)
        print("     清单：…%s" % mine)
        print("     稿件：…%s" % theirs)
    print()
print("  结论：%s" % ("✔ 全部引文逐字可定位" if not bad else "✘ %d 处需修" % len(bad)))