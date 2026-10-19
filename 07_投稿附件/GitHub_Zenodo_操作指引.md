# GitHub + Zenodo 发布操作指引

**状态：A 步（GitHub）已完成 ✅；剩余 B（上线核查）、C（Zenodo DOI）、D（回填）三步，约 15 分钟。**

仓库：<https://github.com/tiantian4634/cross-centre-calibration-drift-icu>

---

## 已完成的部分

| 项目 | 状态 |
|---|---|
| 本地 git 仓库（`09_路B_跨院校准/.git`） | ✅ 已建 |
| 提交历史（10 个提交，分支 `main`） | ✅ 已提交，身份为 Tiantian Zhang |
| **推送到 GitHub** | ✅ **已完成**，本地/远程 HEAD 一致 `5123c3b2` |
| `.gitignore` 排除患者级文件 | ✅ 已验证生效（4 个患者级文件均未入库） |
| 内容级安全扫描（4 个 CSV 逐列检查） | ✅ 无患者 ID、无时间列 |
| 凭据扫描（全部 `.py`） | ✅ 实质命中 0（扫描器自身误报已剔除） |
| `LICENSE`（MIT，Zenodo 必需） | ✅ 已建 |
| `CITATION.cff`（Zenodo 读它预填作者） | ✅ 已填：Zhang Tiantian / Xianju People's Hospital / ORCID 0009-0000-2350-8008 |
| `requirements.txt`（版本已锁） | ✅ 已建 |
| 纳入文件 90 个 / 工作区 6.45 MB | ✅ 远低于 GitHub 限制 |
| **国内网络（git 走代理 20809）** | ✅ 已配 `http.proxy`，推送实测成功 |
| 国内网络 git 调优（HTTP/1.1 等） | ✅ 已设全局配置 |
| 推送辅助脚本 | ✅ `推送前最终核查.py`（DUA 合规全绿）、`推送重试.py`（诊断+重推） |

> 推送前可用 `python 推送前最终核查.py` 复跑一次全绿检查（PhysioNet DUA 合规）。

---

## A. 创建 GitHub 仓库并推送（10 分钟）

### A1. 先填 `CITATION.cff` 的作者信息 ✅ 已完成

已填入：`given-names: Tiantian` / `family-names: Zhang` / `affiliation: Xianju People's
Hospital`（**第一单位**）/ `orcid: https://orcid.org/0009-0000-2350-8008` / `repository-code`
已指向真实 GitHub URL / `preferred-citation` 作者已填（`journal` 仍为占位，确定后补）。

> 为什么必须填：不填的话，Zenodo 会拿你的 GitHub 用户名当作者名，正式引用会变成
> `Zhang, T. (2026). github-username/xxx` 这种形式，期刊编辑会退回来让你改。

> ⚠️ **代码署名 ≠ 论文署名**：此处写张天天（代码是他做的）。论文须为
> 第一作者＝同事、第一单位＝浙江中医药大学（学位要求），张天天任通讯作者。

### A2. 在 GitHub 网页上建一个空仓库 ✅ 已完成

1. 打开 <https://github.com/new>
2. **Repository name**：`cross-centre-calibration-drift-icu`
   （建议用英文，期刊读者和审稿人才搜得到；中文名也可用但不推荐）
3. **Description**：
   > Analysis code, prespecified plans and figures for a multicentre study of
   > calibration drift in acute severity scores (eICU-CRD + MIMIC-IV).
4. **Public** ← 必须选 Public。**Zenodo 只能归档公开仓库**，选 Private 集成会失败。
5. **不要**勾选 Add a README / .gitignore / LICENSE（本地已经有了，勾了会冲突）
6. 点 **Create repository**

### A3. 推送本地代码 ✅ 已完成

**实际走通的路径与原方案不同，以本节为准。**

**不需要 Personal Access Token。** 本机装了 Git for Windows 且已配 `credential.helper = manager`
（Git Credential Manager），推送时直接弹浏览器授权即可。

本地身份、remote、分支名均已在交接前配好，**A3 原列的 `git config user.name` /
`git remote add origin` / `git branch -M` 三步无需重复执行**，直接：

```powershell
cd "E:\文件杂\褚俊智老师\论文选题\选题T1_虚弱营养列线图\09_路B_跨院校准"
git push -u origin main
```

**已推送成功**，本地与远程 HEAD 一致（`5123c3b2`），分支 `main` 跟踪 `origin/main`。

#### ⚠️ 国内网络：**必须走代理**（本次实测结论）

**实测数据（2026-10-19，浙江移动）**：

| 连接方式 | 结果 |
|---|---|
| 直连 TCP `github.com:443` | 0/8 失败 / 8/8 成功（半小时内翻转，**极不可靠**） |
| 直连 HTTPS 单请求 | 18–22 秒（正常应 <1s） |
| 直连 `git push` | **失败**：`Failed to connect to github.com:443 after 21150 ms` |
| **走代理后 `ls-remote`** | **3.0 秒成功** |
| **走代理后 `git push`** | **第 1 次即成功** |

**步骤：先开代理软件 → 再配 git → 再推送。**

```powershell
# 1) 确认代理端口（本机为 mihomo/Clash，口 20808 是 SOCKS、20809 才是 HTTP）
$ie=(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings')
$ie.ProxyServer      # → 127.0.0.1:20809

# 2) 配置 git 走该端口（只认 HTTP 代理）
git config --global http.proxy http://127.0.0.1:20809
```

**关键坑**：Clash/mihomo 通常开两个口——**20809 是 HTTP 口（git 用这个），
20808 是 SOCKS 口（git 用不了，配了会报 `Failed to connect`）**。配错了现象和没配一模一样，
很容易误判成"还是不通"。

**检测代理在不在跑**：
```powershell
Get-NetTCPConnection -LocalPort 20809 -State Listen -ErrorAction SilentlyContinue
# 有输出 = 在跑
```

#### 其余 git 网络调优

```powershell
git config --global http.version HTTP/1.1        # 关键，HTTP/2 经国内链路常被掐
git config --global http.postBuffer 524288000    # 推送 6+ MB 需要
git config --global http.lowSpeedLimit 0         # 关闭低速中断
git config --global http.lowSpeedTime 999999     # 超长容忍
git config --global core.compression 0           # 避免压缩层问题
```

#### 🔒 注意：git 代理配置是**永久**的

`http.proxy` 一旦设了，**以后每次 git 操作都要先开代理**，否则会立刻失败
（git 去连一个不存在的 `127.0.0.1:20809`）。

- **保留**（推荐，已保留）：开代理软件才能推代码/拉代码
- **取消**：`git config --global --unset http.proxy`

**取消方法必须记住**，否则以后换机器或代理卸载后会莫名连不上。

#### ⚠️ PowerShell 会误报失败

`git push 2>&1` 在 PowerShell 下**即使成功也以红字报错**——git 把进度信息写 stderr，
PowerShell 把 stderr 当异常。

**判断成功的唯一标准**：
- 输出里出现 `* [new branch] main -> main`
- 或 `git status -sb` 显示 `## main...origin/main` 且**没有 ahead 字样**

**不要因为红字就重试或以为失败。** 重试本身无害（push 幂等），但会浪费一次 20 秒的连接。

#### 备用：credential.helper 失效时才需要 token

GitHub → 头像 → Settings → Developer settings → Personal access tokens → Tokens (classic)
→ Generate new token，勾 `repo` 和 `public_repo`。

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

**已由脚本验证（`python 推送前最终核查.py` 输出全绿）**
- [x] 仓库里搜不到 `eicu_hospital_context`、`hospital_id_map`
- [x] 仓库里搜不到 `shrinkage_raw`、`learning_curve_raw`
- [x] 4 个待公开 CSV 无患者 ID 列、无时间列
- [x] `CITATION.cff` 里是真实姓名与 ORCID，不是 GitHub 用户名
- [x] README 里写明了「复现需 PhysioNet credentialed 授权」

**需在 GitHub 网页上人工确认**
- [x] 仓库是 **Public**（Zenodo 只能归档公开仓库）
- [x] 搜索 `eicu_hospital_context` → 0 结果（另 `hospital_id_map` 同样 0）
- [x] README 渲染正常
- [x] LICENSE 显示 MIT

> **关于「文件数」**：GitHub 现在的界面**不显示仓库文件总数**——首页标题旁只有
> `NN Commits`（提交数）。曾把「首页显示 90 files」列为核查项是错的，已删除。
>
> **权威文件数只能查 API 或本地**：
> ```powershell
> # 本地（结果应等于 GitHub 上的文件总数）
> (git -c core.quotepath=false ls-files).Count
> ```
> 交接时的数值：**91 个文件 / 6.45 MB / 12 个提交**（2026-10-19）。
> 要在线核对可用 `python 在线核查.py`（走 API，含患者级文件硬红线扫描）。

**Zenodo 完成后回填（3 处）**
- [ ] Zenodo 记录能看到，作者正确，License 是 MIT
- [ ] DOI 已填回 `CITATION.cff` / `README.md` / `Data_Code_Availability.md`
- [ ] 改动已重新提交并推送（`git add -A` → `git commit -m "Add DOI"` → `git push`）

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