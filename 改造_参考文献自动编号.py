# -*- coding: utf-8 -*-
"""把 装配_Manuscript.py 的参考文献从「手写编号列表」改为「键 → 自动编号」。"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

p = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准\装配_Manuscript.py"
t = open(p, encoding="utf-8").read()

start = t.index("# ---------- 6. 参考文献 ----------")
end = t.index("# ---------- 7. 文末段落（仅英文部分） ----------")

NEW = '''# ---------- 6. 参考文献 ----------
# 键 → Nature 格式条目。编号不手写：由正文中首次出现的顺序自动分配，
# 增删引用后不会出现编号错位或参考文献与正文对不上。
REFS = {
    "SOFA": "Vincent, J. L. et al. The SOFA (Sepsis-related Organ Failure Assessment) score to "
            "describe organ dysfunction/failure. *Intensive Care Med.* **22**, 707–710 (1996).",
    "OASIS": "Johnson, A. E. W., Kramer, A. A. & Clifford, G. D. A new severity of illness scale "
             "using a subset of Acute Physiology and Chronic Health Evaluation data elements shows "
             "comparable predictive accuracy. *Crit. Care Med.* **41**, 1711–1718 (2013).",
    "SAPS2": "Le Gall, J. R., Lemeshow, S. & Saulnier, F. A new Simplified Acute Physiology Score "
             "(SAPS II) based on a European/North American multicenter study. *JAMA* **270**, "
             "2957–2963 (1994).",
    "CAL_ACHILLES": "Van Calster, B., McLernon, D. J., van Smeden, M., Wynants, L. & Bossuyt, "
                    "P. M. M. Calibration: the Achilles heel of predictive analytics. *BMC Med.* "
                    "**18**, 88 (2020).",
    "CAL_HIER": "Van Calster, B., Nieboer, D., Vergouwe, Y., De Cock, B., Pencina, M. J. & "
                "Steyerberg, E. W. A calibration hierarchy for risk models was defined: from "
                "utopia to empirical data. *J. Clin. Epidemiol.* **74**, 167–176 (2016).",
    "MIAO": "Miao, Q. et al. Miscalibration of lung allocation models leads to inaccurate waitlist "
            "mortality predictions. *Am. J. Transplant.* **23**, 245–252 (2023).",
    "HAN": "Han, K. et al. Detection of calibration drift in clinical prediction models to inform "
           "model updating. *J. Biomed. Inform.* **111**, 103611 (2021).",
    "BINUYA": "Binuya, M. A. E., Engelhardt, E. G., Schröder, C. P., de Vries, E. G. E. & Braat, "
              "C. H. M. Methodological guidance for the evaluation and updating of clinical "
              "prediction models: a systematic review. *BMC Med. Res. Methodol.* **22**, 317 (2022).",
    "ENSOR": "Ensor, J., Snell, K. I. E., Martin, G. P., Sperrin, M. & Riley, R. D. Individual "
             "participant data meta-analysis for external validation, recalibration, and updating "
             "of a flexible parametric prognostic model. *Stat. Med.* **40**, 3720–3733 (2021).",
    "RILEY_EXT": "Riley, R. D. et al. External validation of prognostic models: what, why, how, "
                 "when and where? *Clin. Kidney J.* **15**, 469–472 (2022).",
    "SAPS3": "Moreno, R. P., Metnitz, P. G. H., Almeida, E., Jordan, B. et al. SAPS 3—From "
             "evaluation of the patient to evaluation of the intensive care unit. Part 2: "
             "Development of a prognostic model for hospital mortality at ICU admission. "
             "*Intensive Care Med.* **31**, 1345–1355 (2005).",
    "ZHANG_LIFELONG": "Zhang, Z. et al. A novel lifelong machine learning-based method to eliminate "
                      "calibration drift in clinical prediction models. *Artif. Intell. Med.* "
                      "**125**, 102256 (2022).",
    "ZHANG_TRANSPORT": "Zhang, Z. et al. Clinical transportability, calibration drift, and local "
                       "updating of a B-mode ultrasound radiomics-clinical prediction model. "
                       "*Gland Surg.* **15**, 1274 (2026).",
    "GEHRINGER": "Gehringer, C. K., Martin, G. P., Sperrin, M., Welch, C. & Riley, R. D. How to "
                 "develop, validate, and update clinical prediction models using multinomial "
                 "logistic regression. *J. Clin. Epidemiol.* **170**, 114–126 (2024).",
    "OGERO": "Ogero, M. et al. Recalibrating prognostic models to improve predictions of "
             "in-hospital child mortality in resource-limited settings. *Paediatr. Perinat. "
             "Epidemiol.* **37**, 257–269 (2023).",
    "SCHNELLINGER": "Schnellinger, E. M. & Yang, W. Comparison of dynamic updating strategies for "
                    "clinical prediction models. *Diagn. Progn. Res.* **5**, 20 (2021).",
    "TANNER": "Tanner, K. T. & Keogh, R. H. Dynamic updating of clinical survival prediction "
              "models in a changing environment. *Diagn. Progn. Res.* **7**, 14 (2023).",
    "ICU_REGISTRY": "Salluh, J. I. F., Quintairos, A., Dongelmans, D. A., Fujii, T. et al. How to "
                    "establish and run a national ICU benchmarking registry. *Curr. Opin. Crit. "
                    "Care* **32**, 523–530 (2026).",
    "MOSER": "Moser, A., Reinikainen, M., Jakob, S. M., Selander, T. A. et al. Mortality prediction "
             "in intensive care units including premorbid functional status improved performance "
             "and internal validity. *J. Clin. Epidemiol.* **142**, 55–63 (2022).",
    "RILEY_SS": "Riley, R. D., Debray, T. P. A., Collins, G. S., Archer, L. et al. Minimum sample "
                "size for external validation of a clinical prediction model with a binary "
                "outcome. *Stat. Med.* **40**, 4230–4251 (2021).",
    "VAN_GELOVEN": "van Geloven, N. et al. Beyond model development in healthcare AI: "
                   "post-development robustness, post-deployment monitoring, and lifecycle "
                   "governance. *Healthcare* **14**, 1459 (2026).",
    "TRIPOD_CLUSTER": "Riley, R. D. et al. Transparent reporting of multivariable prediction models "
                      "developed or validated using clustered data (TRIPOD-Cluster): explanation "
                      "and elaboration. *BMJ* **380**, e071058 (2023).",
    "TRIPOD_AI": "Collins, G. S. et al. TRIPOD+AI statement: updated guidance for reporting "
                 "clinical prediction models that use regression or machine learning methods. "
                 "*BMJ* **385**, e078378 (2024).",
    "STROBE": "von Elm, E., Altman, D. G., Egger, M., Pocock, S. J., Gøtzsche, P. C. & "
              "Vandenbroucke, J. P. The Strengthening the Reporting of Observational Studies in "
              "Epidemiology (STROBE) statement: guidelines for reporting observational studies. "
              "*Ann. Intern. Med.* **147**, 573–577 (2007).",
    "RECORD": "Benchimol, E. I., Smeeth, L., Guttmann, A., Harron, K. et al. The REporting of "
              "studies Conducted using Observational Routinely-collected health Data (RECORD) "
              "statement. *PLoS Med.* **12**, e1001885 (2015).",
    "EICU": "Pollard, T. J., Johnson, A. E. W., Raffa, J. D., Celi, L. A., Mark, R. G. & Badawi, "
            "O. The eICU Collaborative Research Database, a freely available multi-center database "
            "for critical care research. *Sci. Data* **5**, 180178 (2018).",
    "MIMIC": "Johnson, A. E. W. et al. MIMIC-IV, a freely accessible electronic health record "
             "dataset. *Sci. Data* **10**, 1 (2023).",
    "I2": "Higgins, J. P. T. & Thompson, S. G. Quantifying heterogeneity in a meta-analysis. "
          "*Stat. Med.* **21**, 1539–1558 (2002).",
    "DL": "DerSimonian, R. & Laird, N. Meta-analysis in clinical trials. *Control. Clin. Trials* "
          "**7**, 177–188 (1986).",
    "TAU2": "Veroniki, A. A. et al. Methods to estimate the between-study variance and its "
            "uncertainty in meta-analysis. *Res. Synth. Methods* **7**, 55–79 (2016).",
    "EB": "Efron, B. & Morris, C. Data analysis using Stein's estimator and its generalizations. "
          "*J. Am. Stat. Assoc.* **70**, 311–319 (1975).",
}

CITE_RE = re.compile(r"\\[\\[([A-Za-z0-9_]+(?:\\s*,\\s*[A-Za-z0-9_]+)*)\\]\\]")
ORDER = []


def number_citations(text):
    """把 [[KEY]] 换成 [n]，按首次出现顺序编号；返回替换后的文本。"""
    def repl(m):
        nums = []
        for k in [x.strip() for x in m.group(1).split(",")]:
            if k not in REFS:
                raise SystemExit("  ✘ 未定义的文献键：%s" % k)
            if k not in ORDER:
                ORDER.append(k)
            nums.append(ORDER.index(k) + 1)
        return "[" + ",".join(str(n) for n in nums) + "]"
    return CITE_RE.sub(repl, text)


def build_refs():
    unused = [k for k in REFS if k not in ORDER]
    if unused:
        print("  ⚠ 未被正文引用的文献键：%s" % ", ".join(unused))
    return "## References\\n\\n" + "\\n".join("[%d] %s" % (i + 1, REFS[k])
                                             for i, k in enumerate(ORDER))


'''

t = t[:start] + NEW + t[end:]

# 编号调用：clean 之后、拼装之前
anchor = "BACK, LEG, T1 = clean(BACK), clean(LEG), clean(T1)"
assert anchor in t
t = t.replace(anchor,
              anchor + "\n\n"
              "# 引用编号（按正文首次出现顺序；Methods 排在 Discussion 之后，符合 Nature 格式）\n"
              "INTRO, RES, DISC, MET = (number_citations(INTRO), number_citations(RES),\n"
              "                         number_citations(DISC), number_citations(MET))\n"
              "REF = build_refs()\n"
              "print(\"    参考文献 %d 条（按首次出现顺序编号）\" % len(ORDER))", 1)

open(p, "w", encoding="utf-8").write(t)
print("  装配脚本已改为键驱动 + 自动编号")
