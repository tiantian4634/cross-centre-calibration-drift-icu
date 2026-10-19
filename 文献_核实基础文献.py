# -*- coding: utf-8 -*-
"""核实将补入 Methods 的基础文献（评分、数据库、统计方法），避免凭记忆写引用。"""
import io, sys, json, time, urllib.request, urllib.parse, ssl, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROXY = "http://127.0.0.1:20809"
op = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    urllib.request.HTTPSHandler(context=ssl.create_default_context()))
op.addheaders = [("User-Agent", "Mozilla/5.0")]
ES = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

QUERIES = [
    ("SOFA 原始文献", 'SOFA (Sepsis-related Organ Failure Assessment) score[Title] AND 1996[dp]'),
    ("OASIS 原始文献", 'OASIS (Oxford Acute Severity of Illness Score)[Title/Abstract]'),
    ("SAPS-II 原始文献", 'Simplified Acute Physiology Score II[Title] AND 1993[dp]'),
    ("eICU-CRD 数据库", 'eICU Collaborative Research Database[Title]'),
    ("MIMIC-IV 数据库", 'MIMIC-IV[Title] AND Sci Data[ta]'),
    ("DerSimonian-Laird", 'Meta-analysis in clinical trials[Title] AND DerSimonian[au]'),
]


def esearch(term, retmax=5):
    url = ES + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": term, "retmax": retmax, "retmode": "json", "sort": "relevance"})
    with op.open(url, timeout=45) as r:
        d = json.loads(r.read().decode())
    return d["esearchresult"].get("idlist", [])


def efetch(ids):
    if not ids:
        return ""
    url = ES + "efetch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "xml", "rettype": "abstract"})
    with op.open(url, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def strip(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()


print("=" * 96)
print("  基础文献核实（Methods 待补引）")
print("=" * 96)
FOUND = {}
for name, q in QUERIES:
    try:
        ids = esearch(q)
        xml = efetch(ids[:3])
    except Exception as e:
        print("\n[%s] 失败: %s" % (name, str(e)[:60])); continue
    print("\n### %s" % name)
    print("-" * 96)
    for art in re.findall(r"<PubmedArticle>(.*?)</PubmedArticle>", xml, re.S):
        pid = re.search(r"<PMID[^>]*>(\d+)</PMID>", art)
        if not pid:
            continue
        title = re.search(r"<ArticleTitle>(.*?)</ArticleTitle>", art, re.S)
        jr = re.search(r"<Title>(.*?)</Title>", art, re.S)
        yr = re.search(r"<Year>(\d{4})</Year>", art)
        vol = re.search(r"<Volume>([^<]+)</Volume>", art)
        iss = re.search(r"<Issue>([^<]+)</Issue>", art)
        pag = re.search(r"<MedlinePgn>([^<]+)</MedlinePgn>", art)
        doi = re.search(r'<ArticleId IdType="doi">([^<]+)</ArticleId>', art)
        au = re.findall(r"<LastName>([^<]+)</LastName>", art)[:6]
        rec = dict(pmid=pid.group(1), title=strip(title.group(1)) if title else "",
                   journal=strip(jr.group(1)) if jr else "", year=yr.group(1) if yr else "",
                   volume=vol.group(1) if vol else "", issue=iss.group(1) if iss else "",
                   pages=pag.group(1) if pag else "", doi=doi.group(1) if doi else "",
                   authors=au)
        FOUND[name] = rec
        print("  ▸ %s" % rec["title"][:100])
        print("    PMID %s | %s %s;%s(%s):%s" % (rec["pmid"], rec["journal"], rec["year"],
                                                 rec["volume"], rec["issue"], rec["pages"]))
        print("    作者: %s" % ", ".join(au))
        print("    DOI %s" % rec["doi"])
    time.sleep(0.4)

F = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准\文献_基础文献核实.json"
json.dump(FOUND, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n" + "=" * 96)
print("  已核实 %d 组 -> 文献_基础文献核实.json" % len(FOUND))
print("=" * 96)