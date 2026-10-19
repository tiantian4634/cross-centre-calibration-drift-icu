# -*- coding: utf-8 -*-
"""推送器：先诊断代理状态，再推送。

设计要点（2026-10-20 改进）：
  原实现会在代理关闭时盲目重试 10 次后失败，给出的错误信息无法指导行动。
  实测证据：
    · 直连 TCP github.com:443 = 8/8 通，但 git 的 HTTPS 请求（TLS 层）失败
    · 走代理则第 1 次即成功
  因此**代理是必需的**，本工具在代理未运行时立即停止并给出可执行指引，
  不做无意义重试。
"""
import subprocess, time, io, sys, shutil, socket
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
G = shutil.which("git") or "git"
PROXY_PORT = 20809
PROXY = "http://127.0.0.1:%d" % PROXY_PORT


def run(a, timeout=300):
    try:
        p = subprocess.run(a, cwd=B, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"


def port_up(port, host="127.0.0.1"):
    s = socket.socket(); s.settimeout(1.5)
    try:
        s.connect((host, port)); return True
    except Exception:
        return False
    finally:
        s.close()


print("=" * 74)
print("  推送器 · 先诊断后推送")
print("=" * 74)

cfg = subprocess.run([G, "config", "--global", "--get", "http.proxy"],
                     capture_output=True, text=True, encoding="utf-8").stdout.strip()
print("\n[1] 配置状态")
print("    git http.proxy = %s" % (cfg or "（未配置）"))
print("    代理端口 %d    = %s" % (PROXY_PORT, "监听中 ✔" if port_up(PROXY_PORT) else "未监听 ✘"))

if not port_up(PROXY_PORT):
    print("\n" + "=" * 74)
    print("  ✘ 代理未运行 —— 已停止，不做无意义重试")
    print("=" * 74)
    print("""
  诊断：直连 github.com 的 TCP 虽然能连通，但 git 的 HTTPS 请求会被在
        TLS 层拦断（实测直连 push 与 ls-remote 均 exit=128，而走代理
        第 1 次即成功）。**推代码必须开代理。**

  操作：
    1. 打开你的代理软件（mihomo / Clash），确保 %d 端口在监听
    2. 重新运行本脚本

  验证端口：  Get-NetTCPConnection -LocalPort %d -State Listen
""" % (PROXY_PORT, PROXY_PORT))
    sys.exit(2)

if cfg != PROXY:
    print("    ⚠ 与端口不一致 —— 本次以 %s 为准" % PROXY)

print("\n[2] 代理连通性探测 (git ls-remote)")
code, out = run([G, "ls-remote", "--heads", "origin"], 120)
print("    exit=%d  %s" % (code, "✔ 通" if code == 0 else "✘ 不通"))
if code != 0:
    print("    " + next((l for l in out.splitlines() if "fatal" in l), "")[:90])
    sys.exit(3)

print("\n[3] 推送")
for attempt in range(1, 7):
    print("    第 %d 次 ..." % attempt, end=" ", flush=True)
    code, out = run([G, "push", "origin", "main"], 300)
    if code == 0:
        print("✔ 成功"); break
    if "new branch" in out or "Everything up-to-date" in out:
        print("✔ 成功（输出已含成功标志）"); break
    print("✘ %s" % next((l.split(":")[-1].strip() for l in out.splitlines() if "fatal" in l), "失败")[:60])
    time.sleep(min(30, 4 * attempt))
else:
    print("\n    6 次均失败"); sys.exit(4)

print("\n[4] 核验")
_, l = run([G, "rev-parse", "HEAD"], 60)
_, r = run([G, "ls-remote", "origin", "refs/heads/main"], 120)
lh, rh = l.strip(), (r.strip().split()[0] if r.strip() else "（空）")
print("    本地 %s" % lh)
print("    远程 %s" % rh)
print("    %s" % ("✔ 已同步" if lh == rh else "✘ 未同步"))
_, st = run([G, "status", "-sb"], 60)
print("    status: %s" % (st.strip().splitlines()[0] if st.strip() else ""))
print("\n" + "=" * 74)