import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

B = r"E:\文件杂\褚俊智老师\论文选题"
# 只扫描文档类；数据文件（csv/json）是数值本身，不是「叙述里的旧值」
EXT = {".md", ".cff"}
SELF = os.path.basename(__file__)

SIG = re.compile(r"53\.5|23\.4(?!\.\d\s*$)|\+30\.0|\+8\.2|7\.4×10⁻¹³|2\.5×10⁻⁹²|"
                 r"0\.0683|eight-fold|8\s*倍|8倍|53\.0%|\+4\.43|\+8\.20|2\.5254317857068105e-92")
# 需要排除的：说明「这是旧值」的句子、以及本扫描清单本身
CONTEXT = re.compile(r"更正前|更正后|原值|旧值|作废|原先|曾|按原|勿填|→|->|作废值|" 
                     r"shrinkage target|fixed-effect")

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
            if SIG.search(ln) and not CONTEXT.search(ln):
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