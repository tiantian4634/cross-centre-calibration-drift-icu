# -*- coding: utf-8 -*-
"""修复：让预注册文档的写入变为幂等（已存在则不覆盖），并为
学习曲线_预注册.md 补写来源说明 —— 该文件曾因加入缓存功能被脚本重复写入，
导致文件 mtime 被刷新至 11:16（晚于其结果 07:06），时间戳不再可信。
本次仅做记录修复，不改动分析内容、不重跑任何分析。"""
import io, sys, os, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = r"E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
ST = os.path.join(BASE, "03_统计")
NOTE = """

---

## 来源说明（2026-10-19 记录完整性修复）

本文件的内容由 `analysis_learning_curve.py` 的**模块 docstring** 自动生成，docstring 自创建以来未作任何修改。

**⚠️ 时间戳瑕疵（如实记录）**：为加快迭代，该脚本后来加入了结果缓存功能，导致每次运行都会**重写**本文件，
使文件 mtime 刷新至 **2026-10-19 11:16:14**，晚于其结果产物 `learning_curve_raw.csv`（07:06:05）——
**该 mtime 已不能作为"先于结果"的证据**。

**仍可佐证"先于结果"的旁证**：首个产出 `learning_curve_raw.csv`（07:06:05）的那次运行，
其代码流程必然先执行本文件的写入步骤、再进入计算，因此本文件的**内容**在 07:06 之前即已存在。

**修复措施**（`fix_prereg_integrity.py`）：
1. 脚本改为幂等写入——**文件已存在则不覆盖**，从而今后时间戳不再被刷新；
2. 本说明段随文件一并保留，作为该处瑕疵的公开记录。

同批 6 份预注册文档的时间戳未受影响，均可验证地早于对应结果：

| 预注册文档 | 写入时间 | 对应结果产物 | 结果时间 |
|---|---|---|---|
| `路B_预注册.md`（探测轮） | 06:25:26 | I²=75.2%、112 家中心 | 06:25 后 |
| `分析计划_预注册.md` | 06:34:11 | `drift_results.json` | 06:34:27 |
| `学习曲线_预注册.md` | *见上方说明* | `learning_curve_raw.csv` | 07:06:05 |
| `分析计划_第二批.md` | 07:38:50 | `batch2_results.json` | 07:38:53 |
| `分析计划_分析I.md` | 07:56:49 | `shrinkage_raw.csv` | 08:12:05 |
| `分析计划_分析J.md` | 09:41:03 | `mimic_external_summary.json` | 09:41:43 |
| `分析计划_分析K.md` | 10:43:49 | `tau2_framework.json` | 10:43:54 |
"""

p = os.path.join(ST, "学习曲线_预注册.md")
txt = open(p, encoding="utf-8").read()
if "来源说明（2026-10-19 记录完整性修复）" not in txt:
    open(p, "w", encoding="utf-8").write(txt.rstrip() + "\n" + NOTE)
    print("[fixed] 已补写来源说明 ->", p)
else:
    print("[skip] 来源说明已存在")

# 幂等化脚本写入
sp = os.path.join(BASE, "analysis_learning_curve.py")
s = open(sp, encoding="utf-8").read()
old = '''open(os.path.join(ST, "学习曲线_预注册.md"), "w", encoding="utf-8").write(PREREG.replace("{ts}", ts))
print("[pre-reg] 已写入 学习曲线_预注册.md")'''
new = '''_prereg_path = os.path.join(ST, "学习曲线_预注册.md")
if not os.path.exists(_prereg_path):          # 幂等：已存在则不覆盖，保住原始时间戳
    open(_prereg_path, "w", encoding="utf-8").write(PREREG.replace("{ts}", ts))
    print("[pre-reg] 已写入 学习曲线_预注册.md")
else:
    print("[pre-reg] 学习曲线_预注册.md 已存在，保留原始时间戳，不覆盖")'''
if old in s:
    open(sp, "w", encoding="utf-8").write(s.replace(old, new))
    print("[fixed] analysis_learning_curve.py 写入已改为幂等")
else:
    print("[skip] 幂等化目标代码未匹配（可能已被改过）")
