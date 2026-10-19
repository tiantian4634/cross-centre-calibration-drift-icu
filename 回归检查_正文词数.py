# -*- coding: utf-8 -*-
"""正文词数核算（Sci Rep：Intro + Results + Discussion ≤4,500，不含摘要/Methods/参考文献/图注）
   + 三条措辞红线自查。"""
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准\08_正文"


def words(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)      # 去代码块
    t = re.sub(r"\|[\s:|-]+\|", "\n", t)              # 去表格分隔行
    t = re.sub(r"^>?\s*\|", "", t, flags=re.M)        # 去表格行首
    t = re.sub(r"\[\d+(?:,\d+)*\]", "", t)            # 去文内编号引用（Sci Rep 用方括号）
    t = re.sub(r"[*_`#]+", "", t)
    return [w for w in re.findall(r"\S+", t) if re.search(r"[A-Za-z0-9]", w)]


def body(path, heading="## "):
    """取指定二级标题下的正文（去掉文件头部的中文说明块与表格）"""
    txt = open(path, encoding="utf-8").read()
    return txt


files = {
    "Introduction": os.path.join(B, "Introduction_Discussion.md"),
    "Results": os.path.join(B, "Results.md"),
    "Discussion": os.path.join(B, "Introduction_Discussion.md"),
}

txtID = open(files["Introduction"], encoding="utf-8").read()
i_int = txtID.find("## Introduction")
i_disc = txtID.find("## Discussion")
assert i_int > 0 and i_disc > 0
intro_txt = txtID[i_int:i_disc]
disc_txt = txtID[i_disc:]

res_txt = open(files["Results"], encoding="utf-8").read()
r0 = res_txt.find("## Results")
res_body = res_txt[r0:] if r0 > 0 else res_txt

COUNTS = {
    "Introduction": len(words(intro_txt)),
    "Results": len(words(res_body)),
    "Discussion": len(words(disc_txt)),
}
total = sum(COUNTS.values())

print("=" * 84)
print("  正文词数核算（Sci Rep 上限 4,500）")
print("=" * 84)
for k, v in COUNTS.items():
    print("  %-16s %6d 词" % (k, v))
print("  %-16s %6d 词   %s（余 %d 词）"
      % ("合计", total, "✔ 合规" if total <= 4500 else "✘ 超限 " + str(total - 4500),
         4500 - total))
# Results 含表格，粗略给出「去表」估计
res_notab = re.sub(r"(?m)^\|.*\|$", "", res_body)
print("  （Results 若去表格行: %d 词 → 合计 %d 词）"
      % (len(words(res_notab)), total - len(words(res_body)) + len(words(res_notab))))

print("\n" + "=" * 84)
print("  三条措辞红线自查（Introduction + Discussion）")
print("=" * 84)
RED = {
    "归因医疗质量": r"quality of care|医疗质量|质量差异|quality of the care|better quality|worse quality",
    "称外部多中心验证": r"multicentre external validation|multi-center external validation|外部多中心验证",
    "漏掉「非临床推荐」收尾": r"not a clinical recommendation",
}
both = intro_txt + disc_txt
for name, pat in RED.items():
    hits = re.findall(pat, both, re.I)
    if name.startswith("漏掉"):
        print("  %-26s %s" % (name, "✔ 已出现（结论处）" if hits else "✘ 缺失，须补"))
    else:
        print("  %-26s %s" % (name, "✔ 未出现" if not hits else "✘ 出现 %d 次: %s" % (len(hits), hits)))

print("\n" + "=" * 84)
print("  文内引用编号（Nature 格式 [n]）检查")
print("=" * 84)
cites = re.findall(r"\[(\d+(?:,\s*\d+)*)\]", both)
nums = sorted({int(x) for c in cites for x in re.split(r",\s*", c)})
print("  已用引用编号: %s" % nums)
if nums:
    missing = [n for n in range(1, max(nums) + 1) if n not in nums]
    print("  缺号: %s" % (missing if missing else "无 ✔"))
print("  参考文献条数上限: 60（建议）")

print("\n" + "=" * 84)