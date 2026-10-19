# -*- coding: utf-8 -*-
"""把所有预注册文档写入改为幂等（文件已存在则不覆盖），保护原始时间戳。
仅修改写入方式，不改动任何分析内容。"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"

HELPER = '''
def _write_prereg(path, text):
    """幂等写入预注册文档：已存在则不覆盖，以保住『先于结果』的原始时间戳。"""
    if os.path.exists(path):
        print(f"[pre-reg] {os.path.basename(path)} 已存在，保留原始时间戳，不覆盖")
    else:
        open(path, "w", encoding="utf-8").write(text)
        print(f"[pre-reg] 已写入 {os.path.basename(path)}")
'''

TARGETS = {
    "analysis_drift.py": "分析计划_预注册.md",
    "analysis_batch2.py": "分析计划_第二批.md",
    "analysis_shrinkage.py": "分析计划_分析I.md",
    "analysis_mimic_external.py": "分析计划_分析J.md",
    "analysis_tau2_framework.py": "分析计划_分析K.md",
}

for fn, md in TARGETS.items():
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        print(f"[miss] {fn}"); continue
    s = open(p, encoding="utf-8").read()
    if "_write_prereg" in s:
        print(f"[skip] {fn} 已幂等化"); continue
    # 定位形如 open(os.path.join(ST, "X.md"), "w", encoding="utf-8").write( ... ) 的语句
    pat = re.compile(r'open\(\s*os\.path\.join\(ST,\s*"' + re.escape(md) + r'"\)\s*,\s*"w",\s*encoding="utf-8"\s*\)\.write\(',
                     re.S)
    m = pat.search(s)
    if not m:
        print(f"[warn] {fn}: 未匹配到写入语句，跳过"); continue
    # 找到该语句的右括号结束位置（括号配平）
    i = m.end() - 1
    depth = 0
    j = i
    while j < len(s):
        if s[j] == "(":
            depth += 1
        elif s[j] == ")":
            depth -= 1
            if depth == 0:
                break
        j += 1
    call = s[m.start():j + 1]                      # open(...).write( ... )
    inner = call[call.index(".write(") + len(".write("):-1]   # 参数
    new = f'_write_prereg(os.path.join(ST, "{md}"), {inner})'
    s2 = s[:m.start()] + new + s[j + 1:]
    # 插入 helper（放在 import 之后、第一次使用之前）
    anchor = "sys.stdout.reconfigure" if "sys.stdout.reconfigure" in s2 else "sys.stdout = io.TextIOWrapper"
    k = s2.index("\n", s2.index(anchor))
    s2 = s2[:k + 1] + HELPER + s2[k + 1:]
    open(p, "w", encoding="utf-8").write(s2)
    print(f"[fixed] {fn} -> {md}")
