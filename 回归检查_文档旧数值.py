import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

B = r"E:\文件杂\褚俊智老师\论文选题"
# 只扫描文档类；数据文件（csv/json）是数值本身，不是「叙述里的旧值」
EXT = {".md", ".cff"}
SELF = os.path.basename(__file__)

SIG = re.compile(r"53\.5|23\.4(?!\.\d\s*$)|\+30\.0|\+8\.2|7\.4×10⁻¹³|2\.5×10⁻⁹²|"
                 r"0\.0683|eight-fold|8\s*倍|8倍|53\.0%|\+4\.43|\+8\.20|2\.5254317857068105e-92")
# 需要排除的：说明「这是旧值」的句子、引用错误本身的句子、以及未随更正变化的值
CONTEXT = re.compile(r"更正前|更正后|原值|旧值|旧数字|作废|原先|曾|按原|勿填|→|->|作废值|"
                     r"硬编码|首轮|错误|待补|曾误|口径|修订|固定效应|"
                     r"fixed-effect|corrected|original|shrinkage target|disclos")

# 逐值豁免：行内同时出现「该旧值」与「豁免语境」 → 视为合法（未变的现值 / 说明性引用）
ALLOW = [
    # 53.0% = 朴素法 S1 在 m=200 的达标率，未因 ā 权重更正而变化
    (re.compile(r"53\.0%"), re.compile(r"朴素|S1|200|naive|reached")),
]
# 同一行内同时出现旧值与新值 → 必然是「旧 → 新」对照表，合法
OLDV = re.compile(r"53\.5|23\.4(?!\.\d\s*$)|\+30\.0|\+8\.2|7\.4×10⁻¹³|0\.0683")
NEWV = re.compile(r"47\.0|24\.3|\+23\.5|\+9\.05|6\.3×10⁻⁷|3\.7×10⁻¹¹²|\+0\.030")

print("=" * 96)
print("  待更新文档清单（叙述中的旧数值）")
print("=" * 96)
targets = []
for root, dirs, files in os.walk(B):
    dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"} and not d.startswith("_备份")]
    for fn in sorted(files):
        if os.path.splitext(fn)[1].lower() not in EXT or fn == SELF:
            continue
        p = os.path.join(root, fn)
        try:
            lines = open(p, encoding="utf-8").read().split("\n")
        except Exception:
            continue
        hits = []
        for i, ln in enumerate(lines, 1):
            if not SIG.search(ln) or CONTEXT.search(ln):
                continue
            # 豁免一：该旧值在本行同时出现豁免语境（未变的现值 / 说明性引用）
            if any(v.search(ln) and ctx.search(ln) for v, ctx in ALLOW):
                continue
            # 豁免二：同行为「旧值 → 新值」对照表
            if OLDV.search(ln) and NEWV.search(ln):
                continue
            hits.append((i, ln.strip()))
        if hits:
            rel = os.path.relpath(p, B)
            targets.append((rel, hits))
            print("\n  ── %s   (%d 处)" % (rel, len(hits)))
            for i, ln in hits:
                print("    行 %-5d %s" % (i, ln[:120]))

print("\n" + "=" * 96)
print("  需更新的文档: %d 个，合计 %d 处" % (len(targets), sum(len(h) for _, h in targets)))
print("=" * 96)