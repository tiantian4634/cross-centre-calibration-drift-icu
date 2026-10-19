# -*- coding: utf-8 -*-
"""PubMed 第二轮：精确短语与更紧的限定（修正第一轮的噪声）。"""
import io, sys, os, json, time, urllib.request, urllib.parse, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROXY = "http://127.0.0.1:20809"
op = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}),
    urllib.request.HTTPSHandler(context=ssl.create_default_context()))
op.addheaders = [("User-Agent", "Mozilla/5.0 (research literature scan)")]
ES = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

QUERIES = [
    ("R1 精确短语 calibration drift",
     '"calibration drift"[All Fields] AND 2020:2026[dp]'),
    ("R2 重症严重度评分的外部验证",
     '("severity score"[tiab] OR SOFA[tiab] OR APACHE[tiab] OR OASIS[tiab] OR "SAPS"[tiab]) '
     'AND "external validation"[tiab] AND (ICU[tiab] OR "intensive care unit"[tiab]) '
     'AND 2021:2026[dp]'),
    ("R3 重校准所需样本量 / 本地验证的不确定性",
     '("recalibration"[tiab] OR "model updating"[tiab]) AND ("sample size"[tiab] OR '
     'uncertainty[tiab] OR precision[tiab]) AND (prediction[tiab] OR prognostic[tiab]) '
     'AND 2021:2026[dp]'),
    ("R4 TRIPOD / 报告规范与校准",
     '(TRIPOD[tiab] OR "reporting guideline"[tiab]) AND (calibration[tiab] OR '
     '"prediction model"[tiab]) AND 2021:2026[dp]'),
    ("R5 可迁移性 / 通用性（临床预测模型）",
     '(transportab*[tiab] OR generalisab*[tiab] OR generalizab*[tiab] OR "applicability"[tiab]) '
     'AND "prediction model"[tiab] AND (calibration[tiab] OR validation[tiab]) AND 2021:2026[dp]'),
    ("R6 ICU 预测模型的院际表现差异",
     '("intensive care"[tiab] OR ICU[tiab]) AND ("prediction model"[tiab] OR prognostic[tiab]) '
     'AND (calibration[tiab]) AND ("between"[tiab] OR variation[tiab] OR heterogeneit*[tiab]) '
     'AND 2021:2026[dp]'),
    ("R7 随机效应 meta 分析中的收缩与小中心",
     '("shrinkage"[tiab] OR "empirical Bayes"[tiab]) AND ("prediction"[tiab] OR '
     '"performance"[tiab] OR "random-effects"[tiab]) AND (calibration[tiab] OR '
     '"centre"[tiab] OR "hospital"[tiab]) AND 2021:2026[dp]'),
    ("R8 时间验证与模型衰减",
     '("temporal validation"[tiab] OR "model performance over time"[tiab] OR '
     '"performance decay"[tiab] OR "model deterioration"[tiab]) AND 2021:2026[dp]'),
]


def esearch(term, retmax=15):
    url = ES + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": term, "retmax": retmax, "retmode": "json",
         "sort": "relevance"})
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
print("  PubMed 第二轮 · 精确短语 + 紧限定（2021-2026 为主）")
print("=" * 96)

for name, q in QUERIES:
    try:
        total, ids = esearch(q)
        summ = esummary(ids)
    except Exception as e:
        print("\n[%s] 失败: %s" % (name, str(e)[:70])); continue
    print("\n%-44s 命中 %d" % (name, total))
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

F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "文献检索_PubMed第二轮.json")
json.dump(OUT, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n" + "=" * 96)
print("  第二轮 %d 条 -> %s" % (len(OUT), os.path.basename(F)))
print("=" * 96)