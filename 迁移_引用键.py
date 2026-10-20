# -*- coding: utf-8 -*-
"""参考文献扩容第 1 步：把正文里的数字引用改成 [[KEY]] 标记，并插入 9 条新引用。

改完由 装配_Manuscript.py 按首次出现顺序自动编号。
锚点按「空白弹性」正则匹配，避免因为换行位置不同而漏改。
"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
SRC = [os.path.join(B, "08_正文", "Introduction_Discussion.md"),
       os.path.join(B, "08_正文", "Methods.md")]
INTRO, METH = SRC

OLD2KEY = {
    "1": "CAL_ACHILLES", "2": "MIAO", "3": "HAN", "4": "BINUYA", "5": "ENSOR",
    "6": "RILEY_EXT", "7": "ZHANG_LIFELONG", "8": "ZHANG_TRANSPORT",
    "9": "GEHRINGER", "10": "OGERO", "11": "SCHNELLINGER", "12": "TANNER",
    "13": "ICU_REGISTRY", "14": "MOSER", "15": "VAN_GELOVEN",
    "16": "TRIPOD_CLUSTER", "17": "TRIPOD_AI", "18": "SOFA", "19": "SAPS2",
    "20": "EICU", "21": "MIMIC", "22": "DL",
}

DRY = "--write" not in sys.argv


def flex(s):
    """把锚点编译成空白弹性正则。"""
    parts = [re.escape(x) for x in s.split()]
    return re.compile(r"\s+".join(parts))


def migrate(txt):
    def repl(m):
        return "[[%s]]" % ",".join(OLD2KEY[x.strip()] for x in m.group(1).split(","))
    return re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", repl, txt)


INSERTS = [
    (INTRO, "Assessment (SOFA), the Oxford Acute",
     "Assessment (SOFA)[[SOFA]], the Oxford Acute", "SOFA 首现引用"),
    (INTRO, "Severity of Illness Score (OASIS) and the Simplified",
     "Severity of Illness Score (OASIS)[[OASIS]] and the Simplified", "OASIS 首现引用"),
    (INTRO, "Acute Physiology Score II (SAPS-II) are used",
     "Acute Physiology Score II (SAPS-II)[[SAPS2]] are used", "SAPS-II 首现引用"),
    (INTRO, "and it has long been recognised as the more fragile of the two.",
     "and it has long been recognised as the more fragile of the two[[CAL_HIER]].",
     "校准层级"),
    (INTRO, "that the underlying risk adjustment is comparable across them.",
     "that the underlying risk adjustment is comparable across them[[SAPS3]].",
     "SAPS 3 与跨 ICU 基准化"),
    (INTRO,
     "The literature assumes a local sample large enough for the recalibration to be estimated "
     "reliably, and does not typically state what that means in patients. We",
     "The literature assumes a local sample large enough for the recalibration to be estimated\n"
     "reliably. Formal minimum sample sizes have been defined for external validation[[RILEY_SS]],\n"
     "but those criteria address the precision of the calibration estimate, not whether\n"
     "recalibrating improves decisions at a given centre. We",
     "外部验证最小样本量"),
    (INTRO,
     "The quantity the guidance leaves unspecified — how many local patients — appears to be "
     "the parameter that governs whether the recommendation helps.",
     "What those criteria do not address — how many local patients are needed before recalibration\n"
     "helps rather than harms — appears to be the parameter that governs whether the recommendation\n"
     "helps.",
     "衔接改为不与新引文冲突"),
    (INTRO, "We report using STROBE because no prediction model",
     "We report using STROBE[[STROBE]] with the RECORD extension for routinely collected health\n"
     "data[[RECORD]], because no prediction model",
     "STROBE / RECORD"),
    (METH, "the Oxford Acute Severity of Illness Score (OASIS), and the Simplified",
     "the Oxford Acute Severity of Illness Score (OASIS)[[OASIS]], and the Simplified",
     "Methods 中 OASIS 对称补引"),
    (METH, "Heterogeneity was summarised by *I²*, defined as",
     "Heterogeneity was summarised by *I²*[[I2]], defined as", "I² 定义出处"),
    (METH, "Because DerSimonian–Laird predates current guidance, *τ²* was additionally",
     "Because DerSimonian–Laird predates current guidance[[TAU2]], *τ²* was additionally",
     "τ² 估计量比较"),
    (METH, "**S3**, empirical-Bayes shrinkage of the intercept",
     "**S3**, empirical-Bayes shrinkage of the intercept[[EB]]", "EB 收缩出处"),
    (METH, "reported in accordance with the STROBE statement. TRIPOD was **not** used",
     "reported in accordance with the STROBE statement[[STROBE]] and its RECORD extension for\n"
     "routinely collected health data[[RECORD]]. TRIPOD was **not** used",
     "Methods 报告规范"),
    (METH, "estimated by the DerSimonian–Laird method[[DL]]",
     "estimated by the DerSimonian–Laird method [[DL]]", "DL 引用（顺带补空格）"),
]

out = {p: migrate(open(p, encoding="utf-8").read()) for p in SRC}

print("=" * 88)
print("  旧引用 → 键（原文命中情况）")
print("=" * 88)
for p in SRC:
    orig = open(p, encoding="utf-8").read()
    ms = list(re.finditer(r"\[(\d+(?:\s*,\s*\d+)*)\]", orig))
    print("  %-34s %d 处" % (os.path.basename(p), len(ms)))
    for m in ms:
        a = max(0, m.start() - 48)
        print("      %-10s ← …%s" % (m.group(0), orig[a:m.start()].replace("\n", " ")))

print("\n" + "=" * 88)
print("  插入新引用")
print("=" * 88)
for path, old, new, desc in INSERTS:
    pat = flex(old)
    hits = pat.findall(out[path])
    if len(hits) != 1:
        print("  ✘ %-28s 命中 %d 次" % (desc, len(hits)))
        continue
    out[path] = pat.sub(lambda m: new, out[path], count=1)
    print("  ✔ %s" % desc)

if DRY:
    print("\n（dry-run，未落盘。加 --write 执行）")
else:
    for p, t in out.items():
        open(p, "w", encoding="utf-8").write(t)
    print("\n  已写入 %d 个文件" % len(out))
