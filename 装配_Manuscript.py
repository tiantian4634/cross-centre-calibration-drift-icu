# -*- coding: utf-8 -*-
"""按 Scientific Reports 规定的段落顺序，把各文件拼成单一 Manuscript File。

Sci Rep 顺序：标题页 → 摘要 → 关键词 → Introduction → Results（带小标题）→
Discussion（无小标题）→ Methods → References → Author contributions →
Data Availability → Additional Information（Competing interests）→ Funding →
图注（仅正文图，置于 References 之后）→ 表（最后）
"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

B = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
S = os.path.join(B, "08_正文")
OUT = os.path.join(S, "Manuscript.md")


def rd(f):
    return open(os.path.join(S, f), encoding="utf-8").read()


def between(txt, start, end=None):
    i = txt.find(start)
    assert i >= 0, "未找到起点: %s" % start
    j = txt.find(end, i) if end else len(txt)
    if j < 0:
        j = len(txt)
    return txt[i:j].strip()


def clean(txt):
    """去掉中文写作提示、本地文件路径、待办清单等不进稿内容。
    但**保留 ⟨…⟩ 占位符**（作者须填写），只去掉其后的中文说明。"""
    # ① 「⟨X⟩ **【中文说明】**」→ 保留 ⟨X⟩，去掉说明
    txt = re.sub(r"(⟨[^⟩]+⟩)\s*\*\*【[^】]*】\*\*", r"\1", txt)
    txt = re.sub(r"(⟨[^⟩]+⟩)\s*【[^】]*】", r"\1", txt)
    # ② 其余含【…】的行整行删除
    txt = re.sub(r"(?m)^>?\s*\*\*【.*$", "", txt)
    txt = re.sub(r"(?m)^>?\s*【.*$", "", txt)
    # ③ 特定的中文提示行
    for pat in [r"(?m)^>?\s*\(This block is taken from.*$", r"(?m)^>?\s*\*\(正文末尾.*$",
                r"(?m)^>?\s*\*\(本节完成后的自查清单.*$", r"(?m)^>?\s*\*\(占位符.*$",
                r"(?m)^>?\s*（详见.*?\.md.*$"]:
        txt = re.sub(pat, "", txt)
    # ④ 待办清单
    txt = re.sub(r"(?m)^- \[[ x]\] .*$", "", txt)
    txt = re.sub(r"(?m)^#{2,4} 本节完成后的自查清单.*$", "", txt)
    # ⑤ 纯中文说明行（不含 ⟨…⟩ 占位符的）
    def _drop(m):
        line = m.group(0)
        return line if "⟨" in line else ""
    txt = re.sub(r"(?m)^[^\n]*[一-鿿][^\n]*$", _drop, txt)
    # ⑥ 若一行只留下孤立的 ⟨…⟩，保留一行占位
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


# ---------- 1. 标题页 ----------
TITLE = """Discrimination transports, calibration does not: calibration drift in severity scoring
across 187 intensive-care units

⟨First Author Full Name⟩¹, ⟨Second Author Full Name⟩¹, Tiantian Zhang²*

¹ Zhejiang Chinese Medical University, Hangzhou, Zhejiang, China
² Xianju People's Hospital, Zhejiang Southeast Campus of Zhejiang Provincial People's Hospital,
Affiliated Xianju's Hospital, Hangzhou Medical College, Xianju, Taizhou, Zhejiang, China

* Corresponding author. Email: ⟨EMAIL⟩

Corresponding author: Tiantian Zhang, Xianju People's Hospital, Xianju, Taizhou, Zhejiang, China.
Email: ⟨EMAIL⟩"""

# ---------- 2. 摘要 + 关键词 ----------
abs_txt = rd("Abstract_摘要_SciRep版.md")
m = re.search(r"## 摘要（英文投稿版）\n(.*?)\n---", abs_txt, re.S)
ABSTRACT = m.group(1).strip()
km = re.search(r"## 关键词.*?\n\n(.+?)(?:\n\s*\n|$)", abs_txt, re.S)
KEYWORDS = (km.group(1).strip() if km
            else "Intensive care · Calibration · Severity score · External validation · Data drift · Empirical Bayes")

# ---------- 3. Introduction / Discussion ----------
idtxt = rd("Introduction_Discussion.md")
INTRO = between(idtxt, "## Introduction", "## Discussion").strip()
DISC = between(idtxt, "## Discussion").strip()

# ---------- 4. Results（去掉头部映射表） ----------
restxt = rd("Results.md")
RES = between(restxt, "## Results").strip()

# ---------- 5. Methods（去掉头部提示与尾部自查清单） ----------
metxt = rd("Methods.md")
i0 = metxt.find("## Study design and setting")
i1 = metxt.find("## 本节完成后的自查清单")
MET = (metxt[i0:i1] if i1 > 0 else metxt[i0:]).strip()
MET = clean(MET)

# ---------- 6. 参考文献 ----------
REFS = [
 ("1", "Van Calster, B., McLernon, D. J., van Smeden, M., Wynants, L. & Bossuyt, P. M. M. "
       "Calibration: the Achilles heel of predictive analytics. *BMC Med.* **18**, 88 (2020)."),
 ("2", "Miao, Q. et al. Miscalibration of lung allocation models leads to inaccurate waitlist "
       "mortality predictions. *Am. J. Transplant.* **23**, 245–252 (2023)."),
 ("3", "Han, K. et al. Detection of calibration drift in clinical prediction models to inform model "
       "updating. *J. Biomed. Inform.* **111**, 103611 (2021)."),
 ("4", "Binuya, M. A. E., Engelhardt, E. G., Schröder, C. P., de Vries, E. G. E. & Braat, C. H. M. "
       "Methodological guidance for the evaluation and updating of clinical prediction models: a "
       "systematic review. *BMC Med. Res. Methodol.* **22**, 317 (2022)."),
 ("5", "Ensor, J., Snell, K. I. E., Martin, G. P., Sperrin, M. & Riley, R. D. Individual participant "
       "data meta-analysis for external validation, recalibration, and updating of a flexible "
       "parametric prognostic model. *Stat. Med.* **40**, 3720–3733 (2021)."),
 ("6", "Riley, R. D. et al. External validation of prognostic models: what, why, how, when and where? "
       "*Clin. Kidney J.* **15**, 469–472 (2022)."),
 ("7", "Zhang, Z. et al. A novel lifelong machine learning-based method to eliminate calibration drift "
       "in clinical prediction models. *Artif. Intell. Med.* **125**, 102256 (2022)."),
 ("8", "Zhang, Z. et al. Clinical transportability, calibration drift, and local updating of a B-mode "
       "ultrasound radiomics-clinical prediction model. *Gland Surg.* **15**, 1274 (2026)."),
 ("9", "Gehringer, C. K., Martin, G. P., Sperrin, M., Welch, C. & Riley, R. D. How to develop, validate, "
       "and update clinical prediction models using multinomial logistic regression. *J. Clin. "
       "Epidemiol.* **170**, 114–126 (2024)."),
 ("10","Ogero, M. et al. Recalibrating prognostic models to improve predictions of in-hospital child "
       "mortality in resource-limited settings. *Paediatr. Perinat. Epidemiol.* **37**, 257–269 (2023)."),
 ("11","Schnellinger, E. M. & Yang, W. Comparison of dynamic updating strategies for clinical "
       "prediction models. *Diagn. Progn. Res.* **5**, 20 (2021)."),
 ("12","Tanner, K. T. & Keogh, R. H. Dynamic updating of clinical survival prediction models in a "
       "changing environment. *Diagn. Progn. Res.* **7**, 14 (2023)."),
 ("13","How to establish and run a national ICU benchmarking registry. *Curr. Opin. Crit. Care* **32**, "
       "523–530 (2026)."),
 ("14","Mortality prediction in intensive care units including premorbid functional status improved "
       "performance and internal validity. *J. Clin. Epidemiol.* **142**, 55–63 (2022)."),
 ("15","van Geloven, N. et al. Beyond model development in healthcare AI: post-development robustness, "
       "post-deployment monitoring, and lifecycle governance. *Healthcare* **14**, 1459 (2026)."),
 ("16","Riley, R. D. et al. Transparent reporting of multivariable prediction models developed or "
       "validated using clustered data (TRIPOD-Cluster): explanation and elaboration. *BMJ* **380**, "
       "e071058 (2023)."),
 ("17","Collins, G. S. et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction "
       "models that use regression or machine learning methods. *BMJ* **385**, e078378 (2024)."),
 ("18","Vincent, J. L. et al. The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ "
       "dysfunction/failure. *Intensive Care Med.* **22**, 707–710 (1996)."),
 ("19","Le Gall, J. R., Lemeshow, S. & Saulnier, F. A new Simplified Acute Physiology Score (SAPS II) "
       "based on a European/North American multicenter study. *JAMA* **270**, 2957–2963 (1994)."),
 ("20","Pollard, T. J., Johnson, A. E. W., Raffa, J. D., Celi, L. A., Mark, R. G. & Badawi, O. The eICU "
       "Collaborative Research Database, a freely available multi-center database for critical care "
       "research. *Sci. Data* **5**, 180178 (2018)."),
 ("21","Johnson, A. E. W. et al. MIMIC-IV, a freely accessible electronic health record dataset. "
       "*Sci. Data* **10**, 1 (2023)."),
 ("22","DerSimonian, R. & Laird, N. Meta-analysis in clinical trials. *Control. Clin. Trials* **7**, "
       "177–188 (1986)."),
]
REF = "## References\n\n" + "\n".join("[%s] %s" % (n, s) for n, s in REFS)

# ---------- 7. 文末段落（仅英文部分） ----------
BACK = """## Author contributions

**Author contributions.** ⟨逐位作者填写，参照 CRediT 条目：Conceptualisation, Data curation, Formal
analysis, Investigation, Methodology, Software, Validation, Visualisation, Writing – original draft,
Writing – review & editing, Project administration, Supervision, Funding acquisition⟩

## Data Availability

⟨Data Availability 小节待填：须置于 References 之前、正文末尾；含 Zenodo DOI。⟩

## Additional Information

**Competing interests.** ⟨逐位作者声明⟩

**Funding.** This research received no external funding. The article processing charge was covered by
the authors' institution."""

# ---------- 8. 图注（源文件已用投稿编号 Fig.1–7 / SuppFig S1–S3）----------
leg = open(os.path.join(B, "图注_legend.md"), encoding="utf-8").read()
blocks = re.split(r"\n# ", leg)
kept = []
for blk in blocks:
    head = blk.split("\n")[0].strip()
    m = re.match(r"^Figure\s+(\d+)", head)
    if not m:
        continue
    eng = re.search(r"### English legend\s*\n(.*?)(?:\n### |\Z)", blk, re.S)
    if not eng:
        continue
    body = re.sub(r"^>\s?", "", eng.group(1), flags=re.M).strip()
    kept.append((int(m.group(1)), "Figure %d" % int(m.group(1)), body))
kept.sort(key=lambda x: x[0])
LEG = ("## Figure legends\n\n"
       + "\n\n".join("**%s**\n\n%s" % (n, b) for _, n, b in kept))
print("    图注 %d 条: %s" % (len(kept), "; ".join(n for _, n, _ in kept)))

# ---------- 9. Table 1 ----------
tab = rd("Tables_表格.md")
i = tab.find("## Table 1（正文）")
j = tab.find("## Supplementary Table S1")
T1 = tab[i:j].strip()
T1 = T1.replace("## Table 1（正文）—— 三评分的跨中心校准漂移", "## Table 1").strip()

# ---------- 装配 ----------
ABSTRACT = clean(ABSTRACT)
INTRO, RES, DISC, MET = clean(INTRO), clean(RES), clean(DISC), clean(MET)
BACK, LEG, T1 = clean(BACK), clean(LEG), clean(T1)

parts = [
    "# Title Page\n\n" + TITLE,
    "# Abstract\n\n" + ABSTRACT + "\n\n**Keywords.** " + KEYWORDS,
    INTRO, RES, DISC, MET,
    REF, BACK, LEG, T1,
]
man = "\n\n---\n\n".join(p.strip() for p in parts if p and p.strip())
man = re.sub(r"\n{3,}", "\n\n", man)
open(OUT, "w", encoding="utf-8").write(man)

wc = [w for w in re.findall(r"\S+", re.sub(r"[*_`#]+", "", man)) if re.search(r"[A-Za-z0-9]", w)]
print("  ✔ 已生成 %s" % os.path.basename(OUT))
print("    段落数 %d ｜ 全文 %d 词 ｜ %d 行" % (len(parts), len(wc), man.count("\n") + 1))
print("\n    段落顺序（Sci Rep 规定）:")
for k, p in enumerate(parts, 1):
    h = p.strip().split("\n")[0]
    print("      %2d. %s" % (k, h[:78]))
print("\n    正文三节合计（Intro+Results+Discussion）应为 4,316 词，见 回归检查_正文词数.py")