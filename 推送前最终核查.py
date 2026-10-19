import subprocess, os, io, sys, re
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
os.chdir(B)

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", cwd=B).stdout

tracked = [t.strip() for t in sh("git", "-c", "core.quotepath=false", "ls-files").split("\n") if t.strip()]

BLOCK = ["eicu_hospital_context.csv", "hospital_id_map.csv",
         "cohort_eicu.csv", "cohort_mimiciv.csv"]
BIG = ["shrinkage_raw.csv", "learning_curve_raw.csv"]
PID = re.compile(r"^(stay_id|subject_id|patientunitstayid|patienthealthsystemstayid|uniquepid|"
                 r"hadm_id|seqn|patient_id|encounter_id|wardid|apacheadmissiondx|admissionheight|"
                 r"admissionweight|dischargeweight|unitvisitnumber|ethnicity)$", re.I)
TS = re.compile(r"(time|date|offset|intime|outtime|admit|disch)", re.I)

ok = True
print("=" * 68)
print("  推送前最终核查（PhysioNet DUA 合规）")
print("=" * 68)

print("\n[1] 患者级文件是否被排除")
for f in BLOCK:
    inrepo = any(f in t for t in tracked)
    ondisk = os.path.exists(f)
    bad = inrepo
    ok &= not bad
    print("    %-28s 磁盘存在=%-5s 已入库=%-5s  %s"
          % (f, ondisk, bad, "✘ 违规!" if bad else "✔ 已排除"))

print("\n[2] 大体积重抽样明细是否排除出版本控制")
for f in BIG:
    inrepo = any(t.endswith(f) for t in tracked)
    ok &= not inrepo
    print("    %-28s 已入库=%-5s  %s" % (f, inrepo, "✔ 已排除" if not inrepo else "在库(可接受)"))

print("\n[3] 将公开 CSV 的内容级扫描")
csvs = [t for t in tracked if t.lower().endswith(".csv")]
print("    待公开 CSV: %d 个" % len(csvs))
for t in sorted(csvs):
    p = os.path.join(B, t)
    if not os.path.exists(p):
        continue
    d = pd.read_csv(p)
    ids = [c for c in d.columns if PID.match(str(c))]
    tsc = [c for c in d.columns if TS.search(str(c))]
    bad = bool(ids or tsc)
    ok &= not bad
    print("      %-34s 行数 %6d  ID列=%-4s 时间列=%-4s  %s"
          % (t, len(d), ids or "无", tsc or "无", "✘" if bad else "✔"))

print("\n[4] 脚本凭据扫描")
BAD = re.compile(r"(password|passwd|secret|api[_-]?key|Bearer\s)", re.I)
# 扫描器自身含该正则的字面定义，会自我命中，属误报，单独剔除
SELF = {"发布前安全核查.py", "推送前最终核查.py"}
hits, selfhits = [], []
for t in tracked:
    if not t.endswith(".py"):
        continue
    s = open(os.path.join(B, t), encoding="utf-8").read()
    if BAD.search(s):
        (selfhits if os.path.basename(t) in SELF else hits).append(t)
ok &= not hits
print("    实质命中: %d 个  %s" % (len(hits), "✔" if not hits else "✘ " + str(hits)))
if selfhits:
    print("    扫描器自我命中（误报，已剔除）: %s" % ", ".join(selfhits))

print("\n[5] 待推送规模")
total = sum(os.path.getsize(os.path.join(B, t)) for t in tracked
            if os.path.exists(os.path.join(B, t)))
ncommit = int(sh("git", "rev-list", "--count", "HEAD").strip())
print("    文件 %d 个 · %.2f MB · %d 个提交" % (len(tracked), total / 1048576, ncommit))

print("\n" + "=" * 68)
print("  " + ("✔ 全绿 —— 可以推送" if ok else "✘ 存在问题 —— 不要推送"))
print("=" * 68)
print("\n推送命令（在 09_路B_跨院校准 目录下执行）：")
print("    git push -u origin main\n")
print("执行后会弹出浏览器窗口 → 用你的 GitHub 账号点授权 → 回到命令行即完成。")