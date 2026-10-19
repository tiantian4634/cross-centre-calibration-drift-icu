# -*- coding: utf-8 -*-
"""PubMed 第三轮：补齐三个具体缺口 + 关键方法学奠基文献。"""
import io, sys, os, json, time, urllib.request, urllib.parse, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROXY = "http://127.0.0.1:20809"
op = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    urllib.request.HTTPSHandler(context=ssl.create_default_context()))
op.addheaders = [("User-Agent", "Mozilla/5.0 (research literature scan)")]
ES = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

QUERIES = [
    ("T1 eICU 数据库中的校准 / 模型性能",
     '(eICU[All Fields] OR "eICU Collaborative Research Database"[All Fields]) '
     'AND (calibration[All Fields] OR "prediction"[All Fields] OR "mortality model"[All Fields])'),
    ("T2 校准的方法学奠基（Van Calster 等经典）",
     '("calibration"[tiab] AND ("hierarchy"[tiab] OR "recalibration"[tiab] OR '
     '"overfitting"[tiab] OR "well-calibrated"[tiab])) AND (Van Calster[au] OR '
     '"clinical prediction"[tiab]) AND 2019:2026[dp]'),
    ("T3 ICU 内死亡模型的院间表现与基准比较",
     '("mortality"[tiab] OR "risk"[tiab]) AND (benchmark*[tiab] OR "case-mix"[tiab] OR '
     '"standardized mortality ratio"[tiab] OR "observed to expected"[tiab]) AND '
     '(ICU[tiab] OR "intensive care"[tiab]) AND 2019:2026[dp]'),
    ("T4 聚类/多中心数据下模型验证与推断（TRIPOD-Cluster 生态）",
     '("clustered data"[tiab] OR "hierarchical"[tiab] OR "multilevel"[tiab]) AND '
     '"prediction model"[tiab] AND (validation[tiab] OR calibration[tiab]) AND 2021:2026[dp]'),
    ("T5 收缩/先验信息用于小中心估计（临床场景）",
     '(shrinkage[tiab] OR "partial pooling"[tiab] OR "shrinkage estimator"[tiab]) AND '
     '(hospital[tiab] OR "centre"[tiab] OR "risk adjustment"[tiab] OR '
     '"profiling"[tiab]) AND 2019:2026[dp]'),
    ("T6 预测模型的可迁移性与部署后性能监测",
     '("post-deployment"[tiab] OR "monitoring"[tiab] OR "model maintenance"[tiab]) AND '
     '("prediction model"[tiab] OR "clinical AI"[tiab]) AND (calibration[tiab] OR drift[tiab]) '
     'AND 2021:2026[dp]'),
]


def esearch(term, retmax=12):
    url = ES + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": term, "retmax": retmax, "retmode": "json", "sort": "relevance"})
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


OUT = []
print("=" * 96)
print("  PubMed 第三轮 · 补缺 + 奠基文献")
print("=" * 96)
for name, q in QUERIES:
    try:
        total, ids = esearch(q); summ = esummary(ids)
    except Exception as e:
        print("\n[%s] 失败: %s" % (name, str(e)[:70])); continue
    print("\n%-46s 命中 %d" % (name, total))
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
        OUT.append(dict(q=name, pmid=pid, doi=doi, title=t,
                        journal=r.get("source", ""), date=r.get("pubdate", ""),
                        authors=auth))
    time.sleep(0.4)

F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "文献检索_PubMed第三轮.json")
json.dump(OUT, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n" + "=" * 96)
print("  第三轮 %d 条 -> %s" % (len(OUT), os.path.basename(F)))
print("=" * 96)