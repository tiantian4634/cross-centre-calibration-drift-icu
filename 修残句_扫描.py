# -*- coding: utf-8 -*-
"""按段落（而非单行）扫描残句——正文按 ~105 字符硬折行，续行小写属正常。"""
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(B, "装配_Manuscript.py")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("  装配 exit=%s" % r.returncode)

M = open(os.path.join(B, "08_正文", "Manuscript.md"), encoding="utf-8").read()
print("  'kept in sync' 残留: %d（应 0）" % M.count("kept in sync"))
print("  'This block is taken from' 残留: %d（应 0）" % M.count("This block is taken from"))

# ── 段落级扫描 ───────────────────────────────────────────
lines = M.split("\n")
paras, buf, start = [], [], 0
for i, l in enumerate(lines, 1):
    if l.strip():
        if not buf:
            start = i
        buf.append(l.rstrip())
    else:
        if buf:
            paras.append((start, "\n".join(buf)))
            buf = []
if buf:
    paras.append((start, "\n".join(buf)))

SUS = []
for ln, p in paras:
    if p.lstrip().startswith(("|", "```", "#", "![", "<", ">")):
        continue
    flat = re.sub(r"\s+", " ", p).strip()
    plain = re.sub(r"[*`_]", "", flat)
    # a) 段落以小写字母开头（断句残片）
    if plain and plain[0].islower():
        SUS.append((ln, "段落以小写开头", flat))
        continue
    # b) 段落尾是孤立标点组合
    if re.search(r"(\)\*|\)\*\s*)$", flat) and len(flat) < 90:
        SUS.append((ln, "短段落以 )* 结尾", flat))
        continue
    # c) 编辑/占位标记
    if re.search(r"（详见|见上|TODO|XXX|FIXME|待补|占位|intentionally reproduced", flat):
        SUS.append((ln, "占位/编辑标记", flat))
        continue
    # d) 括号不配对
    if flat.count("(") != flat.count(")"):
        SUS.append((ln, "括号不配对 (%d/%d)" % (flat.count("("), flat.count(")")), flat))

print("\n  段落总数 %d ｜ 可疑 %d 处" % (len(paras), len(SUS)))
for ln, why, s in SUS:
    print("    行%-5d [%s]\n           %s" % (ln, why, s[:110]))
if not SUS:
    print("    ✔ 未发现残句")
