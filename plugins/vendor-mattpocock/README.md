# Matt Pocock Skills：按工作阶段选择

> 从 registry/skills.json 生成。编号表示常用阶段，不是必须依次执行的步骤。

每个 skill 仅保存一份；学习、领域建模、测试、交接可以在任何阶段按需进入。

先看 [常用路线](WORKFLOWS.md)，需要 tracker 的项目先看 [项目接入](PROJECT-SETUP.md)。

上游 SKILL.md、配套文档、脚本与资源保持原样。仅 agents/openai.yaml 作 Codex 适配；原始 YAML 保存在 UPSTREAM.lock.json，原始树与打包树分别校验。

## 00-learning · 学习理解

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [teach](skills/00-learning/teach/SKILL.md) | 持续教学：学习目标、资源、课程与学习记录 | 显式调用 |
| [wait-what](skills/00-learning/wait-what/SKILL.md) | 补充背景并用项目术语重新解释 | 显式调用 |

## 10-discovery · 调研与分诊

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [research](skills/10-discovery/research/SKILL.md) | 查阅一手资料并形成有来源的研究记录 | 自动匹配或显式调用 |
| [triage](skills/10-discovery/triage/SKILL.md) | 验证请求并整理可执行的任务说明 | 显式调用 |
| [diagnosing-bugs](skills/10-discovery/diagnosing-bugs/SKILL.md) | 复现故障、定位原因并建立可靠反馈环 | 自动匹配或显式调用 |

## 20-clarification · 需求与决策澄清

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [wayfinder](skills/20-clarification/wayfinder/SKILL.md) | 维护跨会话决策地图，逐步消除不确定性 | 显式调用 |
| [grilling](skills/20-clarification/grilling/SKILL.md) | 通过逐轮提问澄清方案与关键决策 | 自动匹配或显式调用 |
| [grill-me](skills/20-clarification/grill-me/SKILL.md) | 进入 grilling 的显式提问入口 | 显式调用 |
| [grill-with-docs](skills/20-clarification/grill-with-docs/SKILL.md) | 澄清设计并同步沉淀术语和架构决定 | 显式调用 |
| [to-questionnaire](skills/20-clarification/to-questionnaire/SKILL.md) | 为掌握缺失信息的人生成异步问卷 | 显式调用 |

## 30-design · 设计与验证

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [domain-modeling](skills/30-design/domain-modeling/SKILL.md) | 维护领域术语、上下文与架构决策记录 | 自动匹配或显式调用 |
| [codebase-design](skills/30-design/codebase-design/SKILL.md) | 设计深模块、接口与可测试的边界 | 自动匹配或显式调用 |
| [improve-codebase-architecture](skills/30-design/improve-codebase-architecture/SKILL.md) | 探索架构改进候选并展示前后对比 | 显式调用 |
| [prototype](skills/30-design/prototype/SKILL.md) | 用可丢弃原型验证设计问题 | 自动匹配或显式调用 |

## 40-planning · 规格与任务拆分

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [to-spec](skills/40-planning/to-spec/SKILL.md) | 将已有讨论整理成规格并发布到任务载体 | 显式调用 |
| [to-tickets](skills/40-planning/to-tickets/SKILL.md) | 将规格拆成可验证的纵向切片与依赖图 | 显式调用 |

## 50-implementation · 实现与测试

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [implement](skills/50-implementation/implement/SKILL.md) | 依据规格或任务实现、检查、审查并提交 | 显式调用 |
| [tdd](skills/50-implementation/tdd/SKILL.md) | 通过红绿重构建立行为测试与实现闭环 | 自动匹配或显式调用 |

## 60-review-integration · 审查与集成

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [code-review](skills/60-review-integration/code-review/SKILL.md) | 分别审查项目规范与规格符合度 | 自动匹配或显式调用 |
| [resolving-merge-conflicts](skills/60-review-integration/resolving-merge-conflicts/SKILL.md) | 按双方意图解决合并与变基冲突 | 自动匹配或显式调用 |

## 70-handoff · 交接与人工操作

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [handoff](skills/70-handoff/handoff/SKILL.md) | 生成可交给后续 agent 的上下文摘要 | 显式调用 |
| [wizard](skills/70-handoff/wizard/SKILL.md) | 为必须由人完成的操作生成交互向导 | 自动匹配或显式调用 |

## 90-agent-authoring · Agent 文档维护

| Skill | 任务类型 | 调用方式 |
|---|---|---|
| [writing-for-agents](skills/90-agent-authoring/writing-for-agents/SKILL.md) | 改善 agent 文档的触发条件、结构与完成标准 | 自动匹配或显式调用 |

## 技能依赖与项目先决条件

这些是运行时调用依赖，不代表用户需要提前手动执行。分支使用的技能列入依赖，以便安装和移除检查保证流程完整。

| Skill | 调用依赖 | 项目前提 |
|---|---|---|
| `teach` | — | A writable learning workspace for mission, resources, lessons, assets and learning records |
| `triage` | `grilling`, `domain-modeling` | Project issue-tracker configuration; see PROJECT-SETUP.md; Project domain glossary and applicable ADRs |
| `wayfinder` | `grilling`, `domain-modeling`, `research`, `prototype` | Project issue-tracker configuration; see PROJECT-SETUP.md; Project domain glossary and applicable ADRs |
| `grill-me` | `grilling` | — |
| `grill-with-docs` | `grilling`, `domain-modeling` | — |
| `improve-codebase-architecture` | `codebase-design`, `grilling`, `domain-modeling` | — |
| `to-spec` | — | Project issue-tracker configuration; see PROJECT-SETUP.md; Project domain glossary and applicable ADRs |
| `to-tickets` | — | Project issue-tracker configuration; see PROJECT-SETUP.md; Project domain glossary and applicable ADRs |
| `implement` | `tdd`, `code-review` | An implementation spec or tickets; Project checks and authorized commit scope |
| `code-review` | — | Project issue-tracker configuration; see PROJECT-SETUP.md; Project domain glossary and applicable ADRs |

依赖 setup-matt-pocock-skills 的配置要求由项目接入文档说明；该 setup skill 未安装。YAML 不能替代项目配置，也不改变上游发布、提交或教学产物行为。
