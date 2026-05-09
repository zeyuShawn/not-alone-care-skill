<div align="center">

<p><a href="README.md">English</a> | <strong>简体中文</strong></p>

# You Are Not Alone

<p>
  <strong>安全优先、低负担的心理健康支持 Skill：包含危机导航、温和出门恢复、职业方向梳理与本地隐私记录。</strong>
</p>

<p>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img alt="Safety first" src="https://img.shields.io/badge/safety--first-crisis--aware-blue.svg">
  <img alt="Version" src="https://img.shields.io/badge/version-ver2-black.svg">
  <img alt="Local first" src="https://img.shields.io/badge/local--first-privacy--minded-5f4bb6.svg">
</p>

<p>
  <a href="#快速开始">快速开始</a> |
  <a href="#可视化演示">可视化演示</a> |
  <a href="#它能做什么">它能做什么</a> |
  <a href="#一键安装到-vscode--cursor--trae">一键安装</a> |
  <a href="#本地数据与隐私">本地数据与隐私</a> |
  <a href="#安全边界">安全边界</a>
</p>

</div>

---

`not-alone-care-skill` 是一个心理健康支持 Skill，不是诊断工具，不是治疗工具，也不能替代急救、危机热线、医生、心理咨询师或身边可信任的人。

核心原则：人在痛苦、焦虑、低落或慌乱时，不应该再被要求选择复杂模式。助手会先静默做安全路由，给出一个默认的低负担步骤，然后在安全时才引入自助练习、就医准备、支持联系人、温和出门或职业方向模块。

> [!IMPORTANT]
> 如果你或他人可能处于即时危险中，请联系当地急救服务、危机热线或身边可信任的人。本项目只提供辅助性支持与准备工作。

---

## 可视化演示

在 VS Code / Cursor / Trae / Codex 中使用时，可以直接要求：`Use $not-alone-care-skill`。助手会先走安全路由，保持第一步足够小，并且只有在明确同意后才写入本地记录。

![VS Code demo showing the skill prompt, references, scripts, and assistant preview](docs/assets/vscode-demo.svg)

下面两张图分别展示整体架构和安全路由逻辑：

<p align="center">
  <img src="docs/assets/architecture-map.svg" alt="安全路由、引用文档、脚本与隔离数据存储的架构图" width="49%">
  <img src="docs/assets/safety-routing.svg" alt="从用户消息到危机、紧急、照护或自助支持的安全路由流程图" width="49%">
</p>

---

## 快速开始

直接使用 Skill：

```text
Use $not-alone-care-skill to provide safety-first mental-health support, then optionally guide low-burden outing or career clarification when appropriate, and save only consented local records.
```

如果本地 Skill 不可用，可以使用网页版备用 Prompt：

```text
Please follow the uploaded You Are Not Alone Web Prompt. Start with a low-burden check-in and do not ask me to choose a module.
```

初始化本地数据目录：

```bash
python scripts/init_local_data.py
```

追加一条已同意保存的事件记录：

```bash
python scripts/append_event_log.py --field save_consent=true --field session_type=checkin --field mood_score=4 --field anxiety_score=6 --field energy_score=3
```

生成非诊断性的近期趋势摘要：

```bash
python scripts/summarize_trends.py
```

验证本地数据结构：

```bash
python scripts/validate_local_data.py
```

---

## 一键安装到 VSCode / Cursor / Trae

### 本地仓库内一键安装

在当前项目目录运行：

```bash
bash scripts/install.sh --ide all --target "$PWD"
```

它会：

- 将 Skill 安装到 `~/.codex/skills/not-alone-care-skill`，供 Codex 使用。
- 为 VS Code / GitHub Copilot 写入 `.github/copilot-instructions.md`。
- 为 Cursor 写入 `.cursor/rules/not-alone-care-skill.mdc`。
- 为 Trae / Tare 写入 `.trae/rules/project_rules.md`。
- 写入/更新通用 `AGENTS.md`，方便支持 AGENTS.md 的工具读取。

### 从 Git 地址下载并安装

把下面命令里的 URL 换成你的 GitHub 仓库或 fork 地址：

```bash
NAC_REPO_URL="https://github.com/<owner>/not-alone-care-skill.git" bash -c 'tmp="$(mktemp -d)"; git clone --depth 1 "$NAC_REPO_URL" "$tmp"; bash "$tmp/scripts/install.sh" --ide all --target "$PWD"; rm -rf "$tmp"'
```

只安装某些 IDE：

```bash
bash scripts/install.sh --ide vscode,cursor --target "$PWD"
bash scripts/install.sh --ide trae --skip-codex --target "$PWD"
```

---

## 它能做什么

| 模块 | 支持内容 |
| :--- | :--- |
| **第一响应** | 对低落、焦虑、羞耻、孤独、过载给出温和短回复。 |
| **稳定化** | 呼吸/接地、很小的下一步、担忧收纳、低摩擦晚间 check-in。 |
| **危机感知路由** | 自伤、自杀想法、过量服药、伤害他人、严重混乱或不安全处境。 |
| **就医准备** | 为医生、咨询师、学校服务、职场支持、急诊准备简短说明。 |
| **本地记忆** | 可选且需同意的心情记录、每日摘要、支持联系人、趋势摘要。 |
| **网页版备用 Prompt** | 本地 Skill 不可用时，给浏览器 LLM 使用的独立 Prompt。 |
| **Gentle Outing Planner** | 近距离短路线、城市微出行、在条件允许时的跨城/过夜计划。 |
| **Roundtrip Export** | 导出包含 POI 的路线文本、截图友好文本、OCR 文本和本地 HTML。 |
| **Career Compass** | 在低负担前提下梳理职业方向与下一步。 |
| **Job Market Browser** | 在明确同意边界下收集职位信息。 |
| **Local Code Career Profile** | 只分析用户授权的本地项目，提取可证据化技能。 |

---

## 信心、审计与加固

心理健康支持项目不应该宣称字面意义上的“100% 正确”。本仓库通过可审计机制建立事实型信心：明确安全边界、本地写入必须同意、测试覆盖关键隐私行为，并且每次改动后可重复运行验证。

建议循环：

1. 审查架构、Prompt、脚本和数据边界。
2. 运行测试与语法检查。
3. 验证本地数据目录。
4. 对发现的问题做最小修复。
5. 重复直到当前事实证据支持发布。

最近加固点：

- CSV 日志写入前会转义可能被电子表格当作公式执行的单元格。
- profile store 更新/删除需要 `--consent true`。
- 删除日期会先校验格式，并拒绝倒置范围。

---

## 本地数据与隐私

默认路径：

```text
~/not_alone_care_data/
```

| 数据域 | 文件 |
|---|---|
| 心理健康日志 | `event_log.csv`, `daily_summary.csv`, `support_contacts.csv` |
| ver2 出门/职业/职位数据 | `outing_preferences.json`, `career_profile.json`, `job_posts_cache.json`, `exports/roundtrip/` |

隐私默认值：

- 默认保存最小结构化摘要，不保存原始对话文本。
- 每类记录写入前都需要明确同意，除非用户已明确设置持续同意。
- 写入前校验日期、评分范围和字段名。
- CSV 单元格会转义，降低电子表格公式注入风险。
- 心理健康记录不会与外部网站、职位平台或职业数据混用，除非用户明确同意。
- 浏览器收集职位、标准化职位缓存、profile store 更新/删除都需要明确同意。
- 本地代码职业画像默认不保存绝对路径，除非显式使用 `--include-path`。

---

## 安全边界

本项目刻意避免临床越界：

- 不诊断精神障碍。
- 不替代心理咨询、医疗、急救服务或危机热线。
- 不建议开始、停止、增加、减少或替换药物。
- 不提供自伤方法、致命手段、隐瞒建议或详细伤害计划。
- 未经同意不保存本地记录。
- 未经明确同意不向外部服务发送心理健康记录。
- 不自动投递职位、不自动联系招聘方、不自动提交个人信息。

---

## 仓库结构

```text
not-alone-care-skill/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── docs/assets/
│   ├── vscode-demo.svg
│   ├── architecture-map.svg
│   └── safety-routing.svg
├── scripts/
│   ├── install.sh
│   ├── init_local_data.py
│   ├── append_event_log.py
│   ├── validate_local_data.py
│   └── ...
├── references/
├── tests/
└── 网页版/
```

---

## License

MIT License. See [LICENSE](LICENSE).
