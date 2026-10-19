# -*- coding: utf-8 -*-
"""取关键文献的摘要，供 Discussion 做实质性比较。"""
import io, sys, os, json, time, urllib.request, urllib.parse, ssl, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROXY = "http://127.0.0.1:20809"
op = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    urllib.request.HTTPSHandler(context=ssl.create_default_context()))
op.addheaders = [("User-Agent", "Mozilla/5.0")]
ES = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# 按「本研究中的用途」分组
WANT = [
    ("奠基/概念", ["31842878"]),
    ("直接前作（calibration drift）", ["33157313", "35241261", "42591955"]),
    ("重校准与模型更新的方法学", ["36510134", "33768582", "37659584", "38082429",
                            "34865652", "33564405"]),
    ("报告规范（我们为何选 STROBE）", ["36750236", "38626948"]),
    ("重症领域的现状与对照", ["41159833", "41877184", "42400900", "34823021"]),
    ("失校准的临床后果", ["36695624", "40487264"]),
    ("部署后监测 / 趋势", ["42278712"]),
]


def efetch(ids):
    url = ES + "efetch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "xml", "rettype": "abstract"})
    with op.open(url, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def strip(x):
    x = re.sub(r"<[^>]+>", "", x)
    return re.sub(r"\s+", " ", x).strip()


ALL = {}
for group, ids in WANT:
    try:
        xml = efetch(ids)
    except Exception as e:
        print("  取摘要失败 %s: %s" % (group, str(e)[:60])); continue
    for art in re.findall(r"<PubmedArticle>(.*?)</PubmedArticle>", xml, re.S):
        pmid = re.search(r"<PMID[^>]*>(\d+)</PMID>", art)
        if not pmid:
            continue
        pid = pmid.group(1)
        title = re.search(r"<ArticleTitle>(.*?)</ArticleTitle>", art, re.S)
        abst = " ".join(strip(s) for s in
                         re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>", art, re.S))
        jr = re.search(r"<Title>(.*?)</Title>", art, re.S)
        yr = re.search(r"<Year>(\d{4})</Year>", art)
        doi = re.search(r'<ArticleId IdType="doi">([^<]+)</ArticleId>', art)
        ALL[pid] = dict(group=group, pmid=pid,
                        title=strip(title.group(1)) if title else "",
                        journal=strip(jr.group(1)) if jr else "",
                        year=yr.group(1) if yr else "",
                        doi=doi.group(1) if doi else "",
                        abstract=abst[:1400])
    time.sleep(0.4)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "文献_关键摘要.json")
json.dump(ALL, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("=" * 96)
print("  关键文献摘要（共 %d 篇）" % len(ALL))
print("=" * 96)
for group, ids in WANT:
    print("\n### %s" % group)
    print("-" * 96)
    for pid in ids:
        d = ALL.get(pid)
        if not d:
            print("  [%s] 未取到" % pid); continue
        print("  ▸ %s" % d["title"][:110])
        print("    PMID %s | %s %s | %s" % (pid, d["journal"], d["year"], d["doi"]))
        if d["abstract"]:
            print("    摘要: %s%s" % (d["abstract"][:520], "…" if len(d["abstract"]) > 520 else ""))
        else:
            print("    摘要: （PubMed 无结构化摘要）")
print("\n" + "=" * 96)
print("  -> %s" % os.path.basename(OUT))
print("=" * 96)