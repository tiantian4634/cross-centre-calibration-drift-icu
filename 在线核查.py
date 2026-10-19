import json, io, sys, urllib.request, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PROXY = "http://127.0.0.1:20809"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", "Mozilla/5.0"), ("Accept", "application/vnd.github+json")]

REPO = "tiantian4634/cross-centre-calibration-drift-icu"

def get(url):
    with opener.open(url, timeout=60) as r:
        return json.loads(r.read().decode())

print("=" * 66)
print("  GitHub 仓库在线核查（API 权威数据）")
print("=" * 66)

# 1) 仓库元信息
try:
    repo = get(f"https://api.github.com/repos/{REPO}")
    print("\n[1] 仓库信息")
    print("    名称   :", repo["full_name"])
    print("    可见性 :", repo["private"] and "PRIVATE ✘" or "PUBLIC ✔")
    print("    分支   :", repo["default_branch"])
    print("    体积   : %.2f MB" % (repo["size"] / 1024))
    lic = repo.get("license") or {}
    print("    License:", lic.get("spdx_id") or "未识别")
    print("    描述   :", (repo.get("description") or "")[:70])
except Exception as e:
    print("    ✘ 获取失败:", e)

# 2) 递归文件树
tree = get(f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1")
blobs = [t for t in tree["tree"] if t["type"] == "blob"]
dirs = sorted({"/".join(t["path"].split("/")[:-1]) for t in blobs if "/" in t["path"]})
total = sum(t["size"] for t in blobs)

print("\n[2] 文件数量")
print("    ★ GitHub 页面显示的「N Files」= 根目录文件数 + 子目录数")
print("    根目录条目 : %d" % len([t for t in blobs if "/" not in t["path"]]) +
      " 个文件 + %d 个目录" % len([t for t in tree["tree"] if t["type"] == "tree"]))
print("    仓库内文件总数（所有层级）: %d 个，合计 %.2f MB" % (len(blobs), total / 1048576))
print("    子目录 : %s" % ", ".join(d for d in dirs if d))

# 3) 硬红线：敏感文件
print("\n[3] 患者级文件扫描（PhysioNet DUA 合规）")
BANNED = ["eicu_hospital_context.csv", "hospital_id_map.csv",
          "cohort_eicu.csv", "cohort_mimiciv.csv",
          "shrinkage_raw.csv", "learning_curve_raw.csv"]
hit = False
for b in BANNED:
    found = [t["path"] for t in blobs if t["path"].endswith(b)]
    if found:
        hit = True
        print("    ✘ %-30s 存在: %s" % (b, found))
    else:
        print("    ✔ %-30s 不存在" % b)
print("    结论:", "✘ 违规，立刻处理" if hit else "✔ 无患者级文件")

# 4) 逐目录统计
print("\n[4] 分布")
from collections import Counter
c = Counter(t["path"].split("/")[0] if "/" in t["path"] else "(根目录)" for t in blobs)
for k, v in sorted(c.items(), key=lambda x: -x[1]):
    print("    %-26s %3d 个" % (k, v))

# 5) 提交
commits = get(f"https://api.github.com/repos/{REPO}/commits?per_page=100")
print("\n[5] 提交数: %d（GitHub 页面首页只显示最近 5 条）" % len(commits))
for c2 in commits[:3]:
    print("    %s  %s" % (c2["sha"][:8], (c2["commit"]["message"].split("\n")[0])[:64]))

print("\n" + "=" * 66)