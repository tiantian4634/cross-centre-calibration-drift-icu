import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
M = os.path.join(ROOT, "08_正文", "Methods.md")
C = os.path.join(ROOT, "cohort", "README.md")
S = os.path.join(ROOT, "结果汇总_v1.md")

mt = open(M, encoding="utf-8").read()
ct = open(C, encoding="utf-8").read()
st = open(S, encoding="utf-8").read()

print("=" * 88)
print("  Methods 数字校验")
print("=" * 88)

print("\n[1] 队列逐步计数：Methods vs cohort/README.md")
COHORT = ["200,859", "139,367", "71,734", "50,138", "31,307", "30,796",
          "94,458", "65,366", "35,499", "28,607", "8,629", "8,579",
          "3,901", "1,654", "103", "88"]
bad = []
for k in COHORT:
    a, b = k in mt, k in ct
    flag = "✔" if (a and b) else ("⚠" if a else "✘ Methods缺")
    if not (a and b):
        bad.append(k)
    print("    %-9s Methods=%-5s cohort=%-5s %s" % (k, a, b, flag))

print("\n[2] 结果数值：Methods vs 结果汇总_v1.md")
RES = ["+0.030", "0.131", "+0.221", "0.221", "20261019", "100", "200",
       "75.35", "1.8 × 10⁻⁴"]
for k in RES:
    a, b = k in mt, k in st
    print("    %-14s Methods=%-5s 结果汇总=%-5s %s" % (k, a, b, "✔" if a and b else "—"))

print("\n[3] Methods 中出现的关键数字（列出，供人工抽查）")
pat = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?![\w])|(?<![\w.])\d+\.\d+\s*(?:×\s*10⁻?\w+)?")
seen = {}
for m in pat.finditer(mt):
    v = m.group(0)
    seen.setdefault(v, 0)
    seen[v] += 1
for v in sorted(seen, key=lambda x: (0 if "," in x else 1, x))[:46]:
    print("    %-16s ×%d" % (v, seen[v]))

print("\n[4] 占位符与必填项")
for tok, desc in [("⟨ETHICS⟩", "伦理批件号（待用户提供）"),
                  ("⟨COMMITTEE NAME⟩", "伦理委员会名"),
                  ("⟨REFERENCE", "批件号"),
                  ("⟨FULL⟩", "完整正文标记")]:
    print("    %-20s %-6d %s" % (tok, mt.count(tok), desc))

print("\n[5] 三条措辞红线自检")
RED = ["质量差异", "医疗质量", "外部多中心验证", "管理质量", "quality of care"]
for w in RED:
    n = mt.count(w)
    # "not…multicentre external validation" 属于合规用法
    ctx = [l.strip()[:90] for l in mt.split("\n") if w in l]
    print("    %-22s 出现 %d 次 %s" % (w, n, "（见下，须为否定句）" if n else "✔ 未出现"))
    for c in ctx:
        print("        " + c)

print("\n[6] 结构完整性")
for h in ["## Study design and setting", "## Data sources", "## Cohort construction",
          "## Pooled models", "## Centre-level calibration measures",
          "## Between-centre heterogeneity", "## Case-mix ladder",
          "## Temporal stability within hospitals", "## Local recalibration learning curve",
          "## Empirical-Bayes shrinkage", "## Transfer of the shrinkage parameters",
          "## Analysis framework and inferential status", "## Statistical reporting",
          "## Software, seed and reproducibility", "## Ethics", "## Use of a large language model",
          "## Reporting guidelines", "## Data availability"]:
    print("    %s %s" % ("✔" if h in mt else "✘ 缺", h))

print("\n" + "=" * 88)
print("  占位/缺项: %s" % (bad or "队列数字全对"))
print("=" * 88)