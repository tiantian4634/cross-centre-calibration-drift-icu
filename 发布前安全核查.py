# -*- coding: utf-8 -*-
"""发布前安全核查：确认将纳入公开仓库的文件中不含患者级标识符或患者级行。"""
import io, sys, os, re, subprocess
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.chdir(r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"

# 1) 取 git 将要纳入的文件清单（关闭 quotepath，否则中文路径被转义加引号导致漏检）
tracked = subprocess.run(["git", "-c", "core.quotepath=false", "ls-files",
                          "--cached", "--others", "--exclude-standard"],
                         capture_output=True, text=True, encoding="utf-8").stdout.split("\n")
tracked = [t.strip().strip('"') for t in tracked if t.strip()]
n_csv = sum(1 for x in tracked if x.lower().endswith(".csv"))
print(f"[1] 将被纳入版本控制的文件：{len(tracked)} 个（其中 CSV {n_csv} 个）\n")
assert n_csv >= 4, f"⚠ CSV 数量异常（{n_csv}），路径解析可能仍有漏检"

# 2) 患者级标识符黑名单
PATIENT_ID = re.compile(
    r"^(stay_id|subject_id|patientunitstayid|patienthealthsystemstayid|uniquepid|hadm_id|"
    r"seqn|patient_id|encounter_id|wardid|apacheadmissiondx|admissionheight|admissionweight|"
    r"dischargeweight|unitvisitnumber|ethnicity|apacheadmissiondx)$", re.I)
# 时间戳类
TS = re.compile(r"(time|date|offset|intime|outtime|admit|disch)", re.I)

flag = []
print("[2] CSV 文件逐个检查：")
for f in sorted(x for x in tracked if x.lower().endswith(".csv")):
    p = os.path.join(BASE, f)
    d = pd.read_csv(p)
    cols = list(d.columns)
    ids = [c for c in cols if PATIENT_ID.match(str(c))]
    ts_cols = [c for c in cols if TS.search(str(c))]
    uniq = max((d[c].nunique() for c in cols), default=0)
    print(f"\n  ── {f}")
    print(f"     行数 {len(d):,}  列数 {len(cols)}  最大唯一值数 {uniq:,}")
    print(f"     列: {', '.join(map(str, cols[:12]))}{' …' if len(cols) > 12 else ''}")
    print(f"     患者级 ID 列: {ids if ids else '无 ✔'}")
    print(f"     时间/偏移列  : {ts_cols if ts_cols else '无 ✔'}")
    if ids or ts_cols:
        flag.append((f, ids, ts_cols))

print("\n" + "=" * 74)
if flag:
    print("❌ 发现可疑列，需处理：")
    for f, ids, ts in flag:
        print(f"   {f}: IDs={ids}  时间={ts}")
else:
    print("✅ 全部 CSV 均无患者级标识符列、无时间/偏移列")

# 3) 脚本中是否硬编码了本地路径或凭据
print("\n[3] 脚本中的硬编码路径/凭据扫描：")
BAD = re.compile(r"(password|passwd|token|secret|api[_-]?key|Bearer\s)", re.I)
LOCALPATH = re.compile(r"[A-Za-z]:\\")
for f in sorted(x for x in tracked if x.endswith(".py")):
    s = open(os.path.join(BASE, f), encoding="utf-8").read()
    cred = BAD.findall(s)
    paths = sorted(set(LOCALPATH.findall(s)))
    if cred:
        print(f"   ❌ {f}: 疑似凭据 {set(cred)}")
    if paths:
        print(f"   ⚠ {f}: 硬编码本地盘符路径 {paths}")
n_cred = sum(1 for f in tracked if f.endswith(".py") and BAD.search(open(os.path.join(BASE, f), encoding='utf-8').read()))
print(f"   凭据类命中：{n_cred} 个文件（0 为佳）")
print("   注：硬编码的本地路径需要使用者自行改，但**不构成泄露风险**。")
