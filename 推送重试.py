import subprocess, time, io, sys, socket, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
G = shutil.which("git") or "git"


def run(a, timeout=300):
    try:
        p = subprocess.run(a, cwd=B, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"


print("=" * 66)
print("  推送重试器（GitHub 国内间歇性故障）")
print("=" * 66)

# 1) DNS 解析稳定性
print("\n[1] github.com DNS 解析 ×5")
ips = set()
for _ in range(5):
    try:
        ips.add(socket.gethostbyname("github.com"))
    except Exception as e:
        ips.add("FAIL")
    time.sleep(0.3)
print("    解析到的 IP: %s" % ", ".join(sorted(ips)))
if len(ips) > 1:
    print("    ⚠ DNS 结果不稳定 —— 存在解析异常")
else:
    print("    ✔ DNS 稳定")

# 2) TCP 连通性稳定性
print("\n[2] github.com:443 TCP 连通 ×8")
ok = 0
for _ in range(8):
    s = socket.socket()
    s.settimeout(8)
    try:
        s.connect(("github.com", 443))
        ok += 1
    except Exception:
        pass
    finally:
        s.close()
    time.sleep(0.2)
print("    成功 %d/8" % ok)

# 3) ls-remote 探测
print("\n[3] git ls-remote 探测")
code, out = run([G, "-c", "core.quotepath=false", "ls-remote", "--heads", "origin"], 120)
print("    exit=%d  %s" % (code, "✔ 通" if code == 0 else "✘ 不通"))

# 4) 推送重试
print("\n[4] 推送重试（最多 10 次，指数退避）")
for attempt in range(1, 11):
    print("    第 %2d 次 ..." % attempt, end=" ", flush=True)
    code, out = run([G, "push", "origin", "main"], 300)
    if code == 0:
        print("✔ 成功")
        break
    tail = [l for l in out.splitlines() if "fatal" in l or "error" in l]
    print("✘ 失败  %s" % (tail[-1][:70] if tail else "未知"))
    if "new branch" in out or "Everything up-to-date" in out:
        print("    （输出中已含成功标志，实际已推送）")
        break
    wait = min(30, 2 * attempt)
    print("       等待 %ds 后重试" % wait)
    time.sleep(wait)
else:
    print("\n    10 次均失败 —— 请改走下方备用方案")
    sys.exit(1)

# 5) 核验
print("\n[5] 核验")
code, l = run([G, "rev-parse", "HEAD"], 60)
code2, r = run([G, "ls-remote", "origin", "refs/heads/main"], 120)
lh = l.strip()
rh = (r.strip().split()[0] if r.strip() else "（空）")
print("    本地 %s" % lh)
print("    远程 %s" % rh)
print("    %s" % ("✔ 已同步" if lh == rh else "✘ 未同步"))

code3, st = run([G, "status", "-sb"], 60)
print("    status: %s" % st.strip().splitlines()[0] if st.strip() else "")
print("\n" + "=" * 66)
print("  推送命令结束")
print("=" * 66)