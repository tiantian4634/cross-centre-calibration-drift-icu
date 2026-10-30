# -*- coding: utf-8 -*-
"""投稿前参考文献双重核对（ref-autonumber skill 校验模式）
  A) 装配稿直接核：编号闭合 [1..32]、正文首现严格升序、列出=引用、无越界 [n]
  B) skill 脚本独立重编号：按 Sci Rep 阅读顺序拼回 [[KEY]] 源文档 → autonumber_refs.py
     → 键→[n] 映射 与 装配稿逐键比对
"""
import io, sys, os, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

MS = open(r"08_正文\Manuscript.md", encoding="utf-8").read()
SKILL = r"C:\Users\user\.config\opencode\skills\ref-autonumber\scripts\autonumber_refs.py"

# ═══ A. 装配稿直接核 ══════════════════════════════════════
i_refs = MS.find("## References")
body, reflist = MS[:i_refs], MS[i_refs:]

# 引言 list
entries = re.findall(r"^\[(\d+)\]\s", reflist, flags=re.M)
nums = [int(x) for x in entries]
print("== A1 ==")
print("  参考文献列表: %d 条, 编号=%s" % (
    len(nums), nums == list(range(1, len(nums) + 1) and sorted(nums))))

# 正文全部引用（含组合 [1,2] / [9-11]? 本稿用 [a,b] 形式）
cites = re.findall(r"\[([0-9][0-9,]*)\]", body)
flat = []
ok_parse = all("," in c or c.isdigit() for c in cites)
for c in cites:
    flat += [int(x.strip()) for x in c.split(",")]
print("  正文引用标记 %d 处（组合式解析 %s），论及编号范围 %d..%d" % (
    len(cites), "✔" if ok_parse else "✘", min(flat), max(flat)))

# 首现严格升序
first_seq, seen = [], {}
for c in cites:                       # 按标记顺序展开
    for x in [int(y.strip()) for y in c.split(",")]:
        if x not in seen:
            seen[x] = len(seen) + 1
            first_seq.append(x)
print("  首现顺序展开:", first_seq[:40])
ascending = first_seq == list(range(1, 33))
print("  首现严格升序且 1..32 无缺口:", "✔" if ascending else "✘ 需人工复核")
unused = [n for n in range(1, len(nums) + 1) if n not in set(flat)]
print("  列出但未被引用: ", unused or "无 ✔")
out_of = [n for n in set(flat) if n not in range(1, len(nums) + 1)]
print("  正文引用超出列表: ", out_of or "无 ✔")
gaps = [n for n in range(1, len(nums) + 1) if n not in seen]
print("  1..32 中从未首现: ", gaps or "无 ✔")

# ═══ B. skill 脚本独立重编号 ═══════════════════════════════
res_d = {}
ex = {}
pre = open(r"装配_Manuscript.py", encoding="utf-8").read()
seg = pre[pre.find("REFS = {"):]
endbr = seg.find("\n}")
src = seg[:endbr + 2]
exec(src, ex)
REFS = ex["REFS"]
json.dump(REFS, open("_tmp_refs.json", "w", encoding="utf-8"), ensure_ascii=False)

def cut(t, a, b=None):
    i = t.find(a)
    j = t.find(b, i + len(a)) if b and t.find(b, i + len(a)) >= 0 else len(t)
    return t[i:j]

ID = open(r"08_正文\Introduction_Discussion.md", encoding="utf-8").read()
RE = open(r"08_正文\Results.md", encoding="utf-8").read()

# Sci Rep 阅读顺序：Intro → Results → Discussion → Methods（Data Availability 含于 Methods 段）
intro = cut(ID, "## Introduction", "## Discussion")
dism  = cut(ID, "## Discussion")
meths = open(r"08_正文\Methods.md", encoding="utf-8").read()
meths = cut(meths, "## Study design and setting")

doc = baseline = "# s\n\n" + intro + "\n\n" + RE + "\n\n" + dism + "\n\n" + meths
key_id   = sorted(set(re.findall(r"\[\[([A-Za-z0-9_]+(?:\s*,\s*[A-Za-z0-9_]+)*)\]\]", doc)))
undef = sorted({k for grp in key_id for k in grp.split(",")} - set(REFS))
print("== B1 ==")
print("  源文档 [[KEY]] 标记组: %d；独立键数: %d" % (len(key_id), len({k for grp in key_id for k in grp.split(',')})))
print("  未定义键:", undef or "无 ✔")

open("_tmp_source.md", "w", encoding="utf-8").write(doc)
r = subprocess.run([sys.executable, "-X", "utf8", SKILL, "_tmp_source.md", "_tmp_refs.json",
                    "-o", "_tmp_numbered.md"], capture_output=True)
out = r.stdout.decode("utf-8", "replace")
print("  skill 运行 exit=%d" % r.returncode)
for l in out.splitlines():
    if l.strip():
        print("   ", l.strip()[:100])

# 从 skill 输出重编号文档取 回映射
num_doc = open("_tmp_numbered.md", encoding="utf-8").read()
j_refs = num_doc.rfind("## References")
body_num = num_doc[:j_refs]
# [[KEY]] 群在 skill 输出中已替换成 [a,b]；关键 = 位置试读已不可用，改为方法：
# 解析 refs 列表（[k] 条目文本）→ 由条目文本去装配稿 References 查原编号
skill_entries = re.findall(r"^\[(\d+)\]\s+(.*?)$", num_doc[j_refs:], flags=re.M)
asm_entries = re.findall(r"^\[(\d+)\]\s+(.*?)$", MS[i_refs:], flags=re.M)
# 用（卷,页,年）三要素指纹做匹配（防条目文本长且转义差异）
def fingerprint(s):
    s = re.sub(r"\*|\[\[|\]\]", "", s)
    m = re.findall(r"\*\*|\b\d{2,4}\b", s)
    return (" ".join(re.findall(r"\b(19|20)\d{2}\b", s)), re.search(r"page|no", s, re.I) is not None,
            tuple(re.findall(r"\b(\d{2,4})\b", s)[-4:]))
# 直接用全文条目原文比对（装配稿条目应为 skill 条目的同文本）
same_text = {}
asm_by_text = {}
for n_st, t_st in asm_entries:
    asm_by_text[re.sub(r"\s+", " ", t_st.strip())] = int(n_st)
match, fail = 0, []
for n_sk, t_sk in skill_entries:
    key_txt = re.sub(r"\s+", " ", t_sk.strip())
    n_as = asm_by_text.get(key_txt)
    if n_as == int(n_sk):
        match += 1
    else:
        fail.append((n_sk, key_txt[:70], n_as))
print("== B2 ==")
print("  skill 重编号条目: %d；与装配稿同位匹配: %d；不一致: %d" % (
    len(skill_entries), match, len(fail)))
for x in fail[:6]:
    print("   ✘", x)
print("  B3 结论:", "✔ 编号体系（键驱动首现顺序）与装配稿一致" if not fail and ascending and not unused and not out_of else "✘ 存在差异需修")

for f in ["_tmp_refs.json", "_tmp_source.md", "_tmp_numbered.md"]:
    os.remove(f)
