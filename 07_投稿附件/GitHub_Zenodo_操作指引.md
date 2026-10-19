# GitHub + Zenodo 发布操作指引

**状态：** 本地仓库已建好、已提交、已通过安全核查。你只需要完成下面 A–D 四步，全部约 20–30 分钟。

---

## 已经替你做完的部分

| 项目 | 状态 |
|---|---|
| 本地 git 仓库（`09_路B_跨院校准/.git`） | ✅ 已建 |
| 首个提交（commit `29b911f`） | ✅ 已提交 |
| `.gitignore` 排除患者级文件 | ✅ 已验证生效 |
| 内容级安全扫描（4 个 CSV 逐列检查） | ✅ 无患者 ID、无时间列 |
| 凭据扫描（全部 `.py`） | ✅ 0 命中 |
| `LICENSE`（MIT，Zenodo 必需） | ✅ 已建 |
| `CITATION.cff`（Zenodo 读它预填作者） | ⬜ **占位符待你填真实姓名** |
| `requirements.txt`（版本已锁） | ✅ 已建 |
| 纳入文件 84 个 / 工作区 6.42 MB | ✅ 远低于 GitHub 限制 |

---

## A. 创建 GitHub 仓库并推送（10 分钟）

### A1. 先填 `CITATION.cff` 的作者信息

打开 `09_路B_跨院校准\CITATION.cff`，把两处 `⟨FIRST⟩` / `⟨LAST⟩` / `⟨LAST⟩` 换成你的真实姓名。
有 ORCID 就填上（没有可跳过）。

> 为什么必须填：不填的话，Zenodo 会拿你的 GitHub 用户名当作者名，正式引用会变成
> `Zhang, T. (2026). github-username/xxx` 这种形式，期刊编辑会退回来让你改。

### A2. 在 GitHub 网页上建一个空仓库

1. 打开 <https://github.com/new>
2. **Repository name**：`cross-centre-calibration-drift-icu`
   （建议用英文，期刊读者和审稿人才搜得到；中文名也可用但不推荐）
3. **Description**：
   > Analysis code, prespecified plans and figures for a multicentre study of
   > calibration drift in acute severity scores (eICU-CRD + MIMIC-IV).
4. **Public** ← 必须选 Public。**Zenodo 只能归档公开仓库**，选 Private 集成会失败。
5. **不要**勾选 Add a README / .gitignore / LICENSE（本地已经有了，勾了会冲突）
6. 点 **Create repository**

### A3. 推送本地代码

复制 GitHub 页面上那两行带仓库地址的命令，粘贴执行。会提示输入 GitHub 用户名和
**Personal Access Token**（不是密码）。

或者手动执行（在 `09_路B_跨院校准` 目录下）：

```powershell
git remote add origin https://github.com/<你的用户名>/cross-centre-calibration-drift-icu.git
git branch -M main
git push -u origin main
```

> **Token 怎么拿**：GitHub → 头像 → Settings → Developer settings → Personal access
> tokens → Tokens (classic) → Generate new token，勾 `repo` 和 `public_repo`。

---

## B. 上线后必须做的核查（3 分钟，别跳过）

在 GitHub 网页上逐项确认：

| 检查项 | 怎么看 | 期望 |
|---|---|---|
| 文件总数 | 仓库首页 | **84 files** |
| 患者级文件未上传 | 搜索 `eicu_hospital_context` / `hospital_id_map` | **0 结果** |
| 大文件未上传 | 搜索 `shrinkage_raw` / `learning_curve_raw` | **0 结果** |
| README 渲染正常 | 打开仓库首页 | 标题、代码块、表格都正常 |
| LICENSE 识别 | 仓库首页右侧 | 显示 "MIT license" |
| 仓库体积 | Settings → 页面底部 | 约 5–6 MB |

**任意一项不符，立刻停下来处理，不要继续做 Zenodo。**

---

## C. 在 Zenodo 上拿 DOI（10 分钟）

### C1. 关联 GitHub

1. 注册/登录 <https://zenodo.org>（建议绑定 ORCID）
2. 登录后进 <https://zenodo.org/account/settings/applications/>，
   点 **GitHub** → **Configure** → **Authorize**
3. 回到 Zenodo，点右上头像 → **GitHub** → 找到你的仓库 → 把右侧开关拨到 **On**

### C2. 创建一个 Release（这一步才触发 DOI）

1. 回 GitHub 仓库 → 右侧 **Releases** → **Create a new release**
2. **Tag**：`v1.0`（必须填，Zenodo 靠 tag 归档）
3. **Title**：`v1.0 — analysis code for the manuscript`
4. **Description**：粘贴下面这段
5. 勾选 **Set as a pre-release** 不用；直接 **Publish release**

> 建议的 Description：

```
Code, prespecified analysis plans and figures for "Discrimination transports,
calibration does not: cross-centre and temporal drift in acute severity scoring
across 187 ICUs, and the sample size needed to recalibrate".

Contents: 7 prespecified analysis plans (written before execution, with
timestamps); analysis scripts for the drift, learning-curve, temporal-stability,
clinical-impact, empirical-Bayes-shrinkage and tau-squared analyses; figure
generation scripts; and all centre-level result tables.

No patient-level data is redistributed. The cohorts derive from the eICU-CRD and
MIMIC-IV under their respective PhysioNet data use agreements; see README.md.

Licence: MIT (code), CC BY 4.0 (figures and documentation).
```

### C3. 等 DOI 生成

切回 Zenodo 的 GitHub 页面，等几分钟刷新，会出现一条记录。点进去可以看到：

- **DOI**（形如 `10.5281/zenodo.12345678`）—— 这就是你要的
- **Concept DOI** —— 这是整个项目所有版本的 DOI，**引用时优先用这个**

### C4. 补全 Zenodo 元数据（可选但建议）

打开那条记录，检查：Resource type 选 **Software**；作者是否从 `CITATION.cff`
正确带过来了；License 显示 MIT。

---

## D. 把 DOI 填回文档（5 分钟）

一共 **3 处**要改，全在这台机器上：

| 文件 | 改哪里 |
|---|---|
| `CITATION.cff` | `repository-code:` 填 GitHub URL；`preferred-citation` 补 journal 和 doi |
| `README.md` | "Citation" 段落加上 Zenodo badge 和 DOI |
| `07_投稿附件\Data_Code_Availability.md` | 把两处 `⟨to be filled⟩` 换成真实 URL 和 DOI |

Zenodo 会给一段 Markdown badge 代码，直接粘进 `README.md` 顶部：

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12345678.svg)](https://doi.org/10.5281/zenodo.12345678)
```

改完记得再提交一次（见下）。

---

## E. 投稿前最终核查清单

- [ ] GitHub 仓库是 **Public**
- [ ] 仓库里搜不到 `eicu_hospital_context`、`hospital_id_map`
- [ ] 仓库里搜不到 `shrinkage_raw`、`learning_curve_raw`
- [ ] README 里写明了「复现需 PhysioNet credentialed 授权」
- [ ] `CITATION.cff` 里是你的真实姓名，不是 GitHub 用户名
- [ ] Zenodo 记录能看到，作者正确，License 是 MIT
- [ ] DOI 已填回上面那 3 处文件
- [ ] `CITATION.cff` 改动已重新提交并推送（`git add -A` → `git commit -m "Add DOI"` → `git push`）

**第 1、2、3 条是硬性的。** 违反 PhysioNet 数据使用协议的后果比审稿被退严重得多。

---

## 常见问题

**Q：中文文件夹路径推送到 GitHub 会乱码吗？**
不会。git 内部按 UTF-8 存，只是 `git ls-files` 等命令默认会把非 ASCII 路径转义显示（加 `-c core.quotepath=false` 即可看原样）。推送和网页展示都正常。

**Q：能不能把 16 MB 的 `shrinkage_raw.csv` 也传上去？**
可以，走 GitHub Release 的附件功能（单文件上限 2 GB），不要 commit 进 git。它是中心级数据，不含患者标识。

**Q：投稿后代码有改动怎么办？**
在 GitHub 上打新 tag（`v1.1`、`v1.2`），Zenodo 自动为每个版本发新版本 DOI。论文里引用 concept DOI 即可覆盖所有版本。

**Q：期刊只说"code availability"，没提 DOI，还需要 Zenodo 吗？**
不需要，GitHub 链接就够。但已经做了也不吃亏——对学位评审来说这是个可展示的产出。