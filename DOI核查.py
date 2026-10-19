import json, io, sys, time, urllib.request, urllib.error, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

P = "http://127.0.0.1:20809"
ctx = ssl.create_default_context()
op = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": P, "https": P}),
    urllib.request.HTTPSHandler(context=ctx))
op.addheaders = [("User-Agent", "Mozilla/5.0"), ("Accept", "application/json")]

DOI = "10.5281/zenodo.23479142"

def jget(u, tries=3):
    last = None
    for _ in range(tries):
        try:
            with op.open(u, timeout=40) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = e
            time.sleep(3)
    raise last

print("=" * 68)
print("  Zenodo 记录核查  DOI: %s" % DOI)
print("=" * 68)

# 1) DataCite 登记
print("\n[1] DataCite 登记")
try:
    d = jget("https://api.datacite.org/dois/%s" % DOI)
    a = d["data"]["attributes"]
    print("    ✔ 已登记")
    print("    状态       :", a.get("state"))
    print("    类型       :", (a.get("types") or {}).get("resourceTypeGeneral"))
    print("    标题       :", (a.get("titles") or [{}])[0].get("title", "")[:70])
    print("    发布者     :", a.get("publisher"))
    print("    出版年     :", a.get("publicationYear"))
    print("    许可       :", ", ".join(a.get("rightsList") and [r.get("rights","") for r in a["rightsList"]] or ["—"]))
except Exception as e:
    print("    ✘ DataCite 查询失败:", e)

# 2) Zenodo 记录详情（含 concept DOI）
print("\n[2] Zenodo 记录详情")
try:
    z = jget("https://zenodo.org/api/records/%s" % DOI.split("/")[-1])
    meta = z["metadata"]
    print("    ✔ 记录存在")
    print("    标题       :", meta.get("title", "")[:70])
    print("    版本 DOI   :", z.get("doi"))
    print("    concept DOI:", z.get("conceptdoi") or z.get("conceptdoi") or "（首次发布通常与版本 DOI 相同，第二次发布后出现）")
    print("    version    :", meta.get("version") or "—")
    print("    许可       :", meta.get("license") or meta.get("access_right"))
    print("    访问级别   :", meta.get("access_right"))
    print("    创建时间   :", z.get("created"))
    print("\n    作者:")
    for c in meta.get("creators", []):
        print("      - %-22s %s" % (c.get("name", ""), (c.get("affiliation") or "")))
        if c.get("orcid"):
            print("        ORCID: %s" % c["orcid"])
    print("\n    文件:")
    for f in z.get("files", []) or []:
        print("      - %-46s %8.1f KB" % (f.get("key", "?"), (f.get("size") or 0) / 1024))
except Exception as e:
    print("    ✘ Zenodo 查询失败:", e)

# 3) doi.org 解析
print("\n[3] doi.org 解析")
try:
    req = urllib.request.Request("https://doi.org/%s" % DOI, headers={
        "User-Agent": "Mozilla/5.0", "Accept": "text/html", "Accept-Encoding": "identity"})
    # 只跟随 0 次重定向
    class N(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    op2 = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": P, "https": P}),
        urllib.request.HTTPSHandler(context=ctx), N)
    with op2.open(req, timeout=40) as r:
        print("    HTTP %s  Location: %s" % (r.status, r.headers.get("Location")))
except urllib.error.HTTPError as e:
    loc = e.headers.get("Location")
    print("    HTTP %s  Location: %s" % (e.code, loc))
    if loc:
        print("    ✔ 解析到: %s" % loc)
except Exception as e:
    print("    失败:", e)

print("\n" + "=" * 68)
print("  判定：前缀 10.5281 = 真实 Zenodo（DataCite 已登记即可用）")
print("=" * 68)