# -*- coding: utf-8 -*-
"""PubMed 检索：近 5 年（2021-2026）与本研究主题相关的文献。
走 NCBI E-utilities（公开 API，经本地代理）。
"""
import io, sys, os, json, time, urllib.request, urllib.parse, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROXY = "http://127.0.0.1:20809"
op = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    urllib.request.HTTPSHandler(context=ssl.create_default_context()))
op.addheaders = [("User-Agent", "Mozilla/5.0 (research literature scan)")]

ES = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# 近 5 年 + 本研究的六个概念面
QUERIES = [
    ("Q1 校准与外部验证（重症严重度）",
     '("severity score"[tiab] OR "severity scores"[tiab] OR SOFA[tiab] OR OASIS[tiab] OR '
     '"SAPS-II"[tiab] OR APACHE[tiab]) AND calibration[tiab] AND '
     '("external validation"[tiab] OR "external validation" [pt]) AND 2021:2026[dp]'),
    ("Q2 预测模型的重校准与所需样本量",
     'recalibrat*[tiab] AND ("prediction model"[tiab] OR prognostic[tiab]) AND '
     '(sample size[tiab] OR "local validation"[tiab] OR "model updating"[tiab]) AND 2021:2026[dp]'),
    ("Q3 模型校准（TRIPOD 关注的性能维度）",
     'calibration[tiab] AND "prediction model"[tiab] AND (TRIPOD[tiab] OR "reporting"[tiab]) '
     'AND 2021:2026[dp]'),
    ("Q4 跨中心/院际异质性与模型性能漂移",
     '(heterogeneit*[tiab] OR "between-hospital"[tiab] OR "between-centre"[tiab] OR '
     '"inter-centre"[tiab]) AND (calibration[tiab] OR discrimination[tiab]) AND '
     '(mortality[tiab] OR "risk model"[tiab]) AND 2021:2026[dp]'),
    ("Q5 时间漂移 / 数据漂移（临床预测模型）",
     '("temporal validation"[tiab] OR "dataset shift"[tiab] OR "model drift"[tiab] OR '
     '"temporal drift"[tiab] OR "concept drift"[tiab]) AND (prediction[tiab] OR prognostic[tiab]) '
     'AND 2021:2026[dp]'),
    ("Q6 收缩估计 / 经验贝叶斯在 meta 分析与诊断中的应用",
     '("empirical Bayes"[tiab] OR shrinkage[tiab]) AND ("random effects"[tiab] OR '
     '"meta-analysis"[tiab] OR "diagnostic accuracy"[tiab]) AND 2021:2026[dp]'),
]


def esearch(term, retmax=12):
    url = ES + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": term, "retmax": retmax, "retmode": "json",
         "sort": "relevance", "retmax2": retmax})
    with op.open(url, timeout=45) as r:
        d = json.loads(r.read().decode())
    return int(d["esearchresult"].get("count", 0)), d["esearchresult"].get("idlist", [])


def esummary(ids):
    if not ids:
        return {}
    url = ES + "esummary.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "json"})
    with op.open(url, timeout=45) as r:
        return json.loads(r.read().decode()).get("result", {})


ALL = []
print("=" * 96)
print("  PubMed 近 5 年（2021-2026）文献检索 · 6 个概念面")
print("=" * 96)

for name, q in QUERIES:
    try:
        total, ids = esearch(q)
        summ = esummary(ids)
    except Exception as e:
        print("\n[%s] 检索失败: %s" % (name, str(e)[:80]))
        continue
    print("\n%-46s  命中 %d" % (name, total))
    print("-" * 96)
    for i, pid in enumerate(ids, 1):
        r = summ.get(pid, {})
        doi = next((a.get("value") for a in (r.get("articleids") or [])
                    if a.get("idtype") == "doi"), "")
        au = (r.get("authors") or [])[:2]
        auth = ", ".join(a.get("name", "") for a in au)
        if len(r.get("authors") or []) > 2:
            auth += ", et al."
        t = (r.get("title") or "").rstrip(".")
        print("  %2d. %s" % (i, t))
        print("      PMID %s | %s | %s" % (pid, r.get("source", ""), r.get("pubdate", "")))
        if doi:
            print("      DOI %s" % doi)
        print("      %s" % auth)
        ALL.append(dict(q=name, pmid=pid, doi=doi, title=t,
                        journal=r.get("source", ""), date=r.get("pubdate", ""),
                        authors=auth))
    time.sleep(0.4)   # NCBI 限速 3 req/s

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "文献检索_PubMed近5年.json")
json.dump(ALL, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n" + "=" * 96)
print("  合计去重前 %d 条 -> %s" % (len(ALL), os.path.basename(OUT)))
seen = {}
for r in ALL:
    seen.setdefault(r["pmid"], r)
print("  按 PMID 去重后 %d 条" % len(seen))
print("=" * 96)