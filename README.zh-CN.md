<div align="center">

<p><a href="README.md">English</a> | <strong>简体中文</strong></p>

# You Are Not Alone

<h3>面向 AI 助手的安全优先 mental-care 支持 —— 已接入 OpenClaw 机器人入口。</h3>

<p>
  在难熬时先给用户一个稳定的小步骤：先做安全路由，再准备求助沟通、轻松出门、职业压力梳理，并把敏感记录留在本地。
</p>

<p>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img alt="Version" src="https://img.shields.io/badge/version-2.0.0-black.svg">
  <img alt="OpenClaw" src="https://img.shields.io/badge/OpenClaw-bot%20gateway-ff6b35.svg">
  <img alt="Safety first" src="https://img.shields.io/badge/safety--first-crisis--aware-blue.svg">
  <img alt="Local first" src="https://img.shields.io/badge/local--first-privacy--minded-5f4bb6.svg">
</p>

<p>
  <a href="#openclaw-优先入口">OpenClaw 优先入口</a> ·
  <a href="#为什么团队会想用它">为什么使用</a> ·
  <a href="#可视化演示">可视化演示</a> ·
  <a href="#安装">安装</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#它能做什么">它能做什么</a> ·
  <a href="#本地数据与隐私">隐私</a> ·
  <a href="#安全边界">安全</a>
</p>

</div>

---

## OpenClaw 优先入口

> **2.0.0 新增：** 一条命令把飞书/Lark、Discord、Telegram、Slack、WhatsApp、Teams，以及其他 OpenClaw 渠道机器人接成专门的 mental-care 入口。

```bash
bash scripts/install_openclaw.sh --channel telegram --bot-id mental-care-telegram --consent true
```

这会带来什么：

- **在用户已经使用的聊天渠道里出现** —— 将 OpenClaw 支持的机器人路由到同一套安全优先工作流。
- **指定专属护理专员** —— 用 `scripts/configure_openclaw_bot.py` 把某个已有机器人标记为 mental-care 专员。
- **Skill 不保存密钥** —— 本地只保存非密钥路由元数据；bot token、模型 key、渠道密钥留在 OpenClaw 或服务商密钥系统中。
- **继续本地优先** —— 心理健康日志与渠道元数据隔离，写入前必须获得明确同意。

---

## 为什么团队会想用它

`mental-care-skill` 是一个心理健康支持 Skill，不是诊断工具或治疗工具。当前仓库版本：`2.0.0`（也记录在 `VERSION`）。

产品承诺很简单：人在痛苦、焦虑、低落或慌乱时，不应该再被要求选择复杂模式，也不需要把所有事情讲得完美。助手会先静默做安全路由，给出一个默认的低负担步骤，然后在合适时打开可选路径。

| 产品结果 | 用户价值 |
| :--- | :--- |
| **降低认知负担** | 温和短回复，只给一个做得到的默认步骤。 |
| **更安全的路由** | 自伤、自杀想法、过量服药、严重混乱、即时危险等信号优先处理。 |
| **可执行的后续动作** | 帮用户为医生、咨询师、学校服务、职场支持、可信任的人或急救服务准备简短说明。 |
| **私密的连续性** | 可选本地记录用于趋势和复盘；写入前检查同意，默认不保存原始对话。 |
| **多渠道入口** | OpenClaw 机器人可成为 mental-care 入口，同时不把敏感记录搬进聊天渠道。 |

> [!IMPORTANT]
> 本项目不是诊断工具，不是心理咨询师，也不能替代急救、危机热线、医生、心理咨询师或身边可信任的人。如果你或他人可能处于即时危险中，请联系当地急救服务、危机热线或身边可信任的人。

---

## 可视化演示

在 VS Code / Codex 中使用时，可以直接要求：`Use $mental-care-skill`。助手会加载安全优先工作流，保持第一步足够小，并且只有在明确同意后才写入本地记录。

![VS Code demo showing the skill prompt, references, scripts, and assistant preview](docs/assets/vscode-demo.svg)

下面两张图展示产品全貌：架构图说明 references、scripts 和隔离本地存储如何协作；安全路由图说明为什么危机和紧急照护逻辑总是在出门或职业模块之前运行。

<p align="center">
  <img src="docs/assets/architecture-map.svg" alt="安全路由、引用文档、脚本与隔离数据存储的架构图" width="49%">
  <img src="docs/assets/safety-routing.svg" alt="从用户消息到危机、紧急、照护或自助支持的安全路由流程图" width="49%">
</p>

---

## 安装

安装到 Codex，并同时写入主流 AI IDE 桥接文件（VS Code/Copilot、Cursor、Trae/Tare 和 AGENTS.md）：

```bash
bash scripts/install.sh --ide all --target "$PWD"
```

从 Git 地址一键下载并安装（把 URL 换成你的 fork 或发布仓库）：

```bash
MENTAL_CARE_REPO_URL="https://github.com/<owner>/mental-care-skill.git" bash -c 'tmp="$(mktemp -d)"; git clone --depth 1 "$MENTAL_CARE_REPO_URL" "$tmp"; bash "$tmp/scripts/install.sh" --ide all --target "$PWD"; rm -rf "$tmp"'
```

只安装部分 IDE 集成：

```bash
bash scripts/install.sh --ide vscode,cursor --target "$PWD"
bash scripts/install.sh --ide trae --skip-codex --target "$PWD"
```

---

## 快速开始

直接使用 Skill：

```text
Use $mental-care-skill to provide safety-first mental-health support, then optionally guide low-burden outing or career clarification when appropriate, and save only consented local records.
```

使用网页版备用 Prompt：

```text
Please follow the uploaded You Are Not Alone Web Prompt. Start with a low-burden check-in and do not ask me to choose a module.
```

初始化并验证本地数据目录：

```bash
python scripts/init_local_data.py
python scripts/validate_local_data.py
```

追加一条已同意保存的事件记录：

```bash
python scripts/append_event_log.py --field save_consent=true --field session_type=checkin --field mood_score=4 --field anxiety_score=6 --field energy_score=3
```

生成非诊断性的近期趋势摘要：

```bash
python scripts/summarize_trends.py
```

---

## OpenClaw 机器人安装

OpenClaw 只作为聊天渠道网关，`mental-care-skill` 仍然负责安全策略。项目支持通过代码把飞书/Lark、Discord、Telegram、Slack、WhatsApp、Teams 等 OpenClaw 渠道机器人接成 mental-care 入口。

安装 bridge，并把某个机器人标记为专门的 mental-care 护理专员：

```bash
bash scripts/install_openclaw.sh --channel telegram --bot-id mental-care-telegram --consent true
```

用同一条命令运行 OpenClaw 网关安装和 onboarding：

```bash
bash scripts/install_openclaw.sh --install-gateway --onboard --channel feishu --bot-id feishu-care --consent true
```

不重装 bridge，只设置或更新某个已有 OpenClaw 机器人：

```bash
python scripts/configure_openclaw_bot.py set \
  --bot-id mental-care-discord \
  --channel discord \
  --display-name "Mental Care" \
  --allowed-user-ids '["123456"]' \
  --consent true
```

本地数据库文件是 `~/mental_care_data/openclaw_dedicated_bots.json`。它只保存非密钥路由信息；机器人 token、模型 API key、渠道密钥应保存在 OpenClaw 或服务商密钥系统中。

---

## 它能做什么

| 模块 | 支持内容 |
| :--- | :--- |
| **第一响应** | 对低落、焦虑、羞耻、孤独、过载给出温和短回复。 |
| **稳定化** | 呼吸/接地、很小的下一步、担忧收纳、低摩擦晚间 check-in。 |
| **危机感知路由** | 自伤、自杀想法、过量服药、伤害他人、严重混乱或不安全处境。 |
| **就医准备** | 为医生、咨询师、学校服务、职场支持、急诊准备简短说明。 |
| **本地记忆** | 可选且需同意的心情记录、每日摘要、支持联系人、趋势摘要。 |
| **OpenClaw Bot (2.0.0)** | 通过一条命令安装 OpenClaw bridge，并在本地指定专门的 mental-care 护理机器人。 |
| **Gentle Outing Planner (2.0.0)** | 近距离短路线、城市微出行、在条件允许时的跨城/过夜计划。 |
| **Roundtrip Export (2.0.0)** | 导出包含 POI 的路线文本、截图友好文本、OCR 文本和本地 HTML。 |
| **Career Compass (2.0.0)** | 在低负担前提下梳理职业方向与下一步。 |
| **Job Market Browser (2.0.0)** | 在明确同意边界下收集职位信息。 |
| **Local Code Career Profile (2.0.0)** | 只分析用户授权的本地项目，提取可证据化技能。 |
| **网页版备用 Prompt** | 本地 Skill 不可用时，给浏览器 LLM 使用的独立 Prompt。 |

---

## 演示

### 演示 1：核心低负担支持

```text
User: I have been anxious for days and I don't know whether I should see someone.
Assistant: That sounds exhausting. I cannot diagnose this, but several days of anxiety is worth bringing to a professional. If you want, I can help make a short care note: how long it has lasted, what changed in sleep/appetite, how it affects your day, and what you want to ask.
```

### 演示 2：OpenClaw 专属机器人

```bash
bash scripts/install_openclaw.sh --channel discord --bot-id team-care-bot --consent true
python scripts/configure_openclaw_bot.py list
```

### 演示 3：轻松出门规划

```text
User: I feel trapped at home and my head is too full.
Assistant: You do not need to solve everything right now. Let's make one low-burden environment shift: a 40-minute route with one open-air point, one sit-down point, and an easy return option.
```

### 演示 4：职业方向 + 岗位匹配

```text
User: I feel stuck professionally, but job searching makes me panic.
Assistant: Let's keep this low-pressure. We can do two tracks: identify what your current projects already prove, or compare one small set of real job posts. You only need to choose one first step.
```

### 演示 5：往返行程导出流程

```bash
python scripts/export_roundtrip_itinerary.py --itinerary itinerary.json
python scripts/validate_itinerary_export.py --itinerary itinerary.json --export-dir ~/mental_care_data/exports/roundtrip/2026-04-25-example
```

---

## 信心、审计与加固

心理健康支持项目不应该宣称字面意义上的“100% 正确”。本仓库通过可审计机制建立事实型信心：明确安全边界、本地写入必须同意、测试覆盖关键隐私行为，并且每次改动后可重复运行验证。

建议发布循环：

1. 审查架构、Prompt、脚本和数据边界。
2. 运行测试与语法检查。
3. 验证本地数据目录。
4. 在临时目录测试 OpenClaw bridge 安装。
5. 对任何问题做最小可信修复，然后重复，直到当前事实证据支持发布。

最近加固点：

- CSV 日志写入前会转义可能被电子表格当作公式执行的单元格。
- profile store 更新/删除需要 `--consent true`。
- 删除日期会先校验格式，并拒绝倒置范围。
- OpenClaw bot 路由只保存非密钥元数据，且设置/删除必须显式同意。

---

## 网页版 Prompt

如果本地脚本不可用，可以使用独立浏览器 Prompt：

- Prompt 文件：[网页版/mental-care-web-prompt.md](网页版/mental-care-web-prompt.md)

网页版 Prompt 面向浏览器 LLM 使用，并避免假装自己能写入本地文件。

---

## 本地数据与隐私

默认本地路径：

```text
~/mental_care_data/
```

| 数据域 | 文件 |
|---|---|
| 心理健康日志 | `event_log.csv`, `daily_summary.csv`, `support_contacts.csv` |
| 2.0.0 出门/职业/职位/OpenClaw 数据 | `outing_preferences.json`, `career_profile.json`, `job_posts_cache.json`, `openclaw_dedicated_bots.json`, `exports/roundtrip/` |

隐私默认值：

- 默认保存最小结构化摘要，不保存原始对话文本。
- 每类记录写入前都需要明确同意，除非用户已明确设置持续同意。
- 写入前校验日期、评分范围和字段名。
- CSV 单元格会转义，降低电子表格公式注入风险。
- 用户可以检查、摘要、更新、验证、dry-run 删除或删除记录。
- 心理健康记录不会与外部网站、职位平台、职业数据或 OpenClaw 渠道元数据混用，除非用户明确同意。
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

<details open>
<summary><strong>查看仓库结构</strong></summary>

```text
mental-care-skill/
├── README.md
├── README.zh-CN.md
├── VERSION
├── SKILL.md
├── docs/assets/
│   ├── vscode-demo.svg
│   ├── architecture-map.svg
│   └── safety-routing.svg
├── references/
│   ├── openclaw-integration.md
│   ├── triage-router.md
│   ├── crisis-protocol.md
│   └── ...
├── scripts/
│   ├── install.sh
│   ├── install_openclaw.sh
│   ├── configure_openclaw_bot.py
│   ├── init_local_data.py
│   ├── validate_local_data.py
│   └── ...
├── tests/
└── 网页版/
```

</details>

---

## 建议 GitHub Topics

```text
mental-health
mental-health-chatbot
openclaw
llm
ai-companion
crisis-support
suicide-prevention
anxiety
depression
self-help
prompt-engineering
local-first
privacy
career-guidance
travel-planning
```

---

## License

MIT License. See [LICENSE](LICENSE).
