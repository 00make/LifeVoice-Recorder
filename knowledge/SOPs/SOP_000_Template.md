---
id: "SOP_Template_v1"
schema_version: "1.0"
name: "Standard Operating Procedure Template"
author: "LifeOS Architect"
created_at: "2026-02-12"
description: "模板文件：定义 Agent 如何执行标准任务。所有 SOP 必须遵循此格式以便 Orchestrator 解析。"

# 触发条件 (Orchestrator 路由依据)
# 支持 Context 逻辑运算
triggers:
  - type: "time"
    cron: "0 9 * * *"
  - type: "context"
    condition: "Location == 'Office' AND State.Energy > 70"
  - type: "event"
    name: "user.intent.detected"
    params: { keyword: "template" }

# 所需角色与其配置 (Dynamic Swarm Config)
roles:
  - id: "executor"
    type: "worker"
    model: "qwen2.5-14b-instruct-quant"
    temperature: 0.3
  - id: "critic"
    type: "reviewer"
    model: "gpt-4o"
    temperature: 0.1

# 资源预算
budget:
  max_tokens: 4000
  max_cost_usd: 0.1
  timeout_sec: 60
---

# 1. 任务目标 (Objective)

清晰描述此 SOP 旨在解决什么问题。
*Example: 将原始语音笔记转化为结构化的 Obsidian 卡片。*

# 2. 执行步骤 (Execution Steps)

Orchestrator 将按顺序解析以下步骤，并注入到对应 Agent 的 System Prompt 中。

## Step 1: [步骤名称]

- **Assignee**: `executor`
- **Action Type**: `Generation` | `ToolCall` | `Search`
- **Tools**: [`search_tool`, `python_repl`] (Optional)
- **Input Context**:
  - `{{global_context}}`
  - `{{previous_step.output}}`
- **Instruction Prompt**:
  > 请详细描述 Agent 在此步骤需要做什么。
  > 应当包含具体的输出格式要求。

## Step 2: [步骤名称] (Quality Check)

- **Assignee**: `critic`
- **Action Type**: `Review`
- **Input Context**: `{{step_1.output}}`
- **Validation Rules**:
  1. 必须包含 JSON 格式的输出。
  2. 必须没有幻觉。
- **Failure Handling**:
  - `If Score < 3`: Retry Step 1 with Feedback.
  - `If Score >= 3`: Proceed to Next.

# 3. 最终交付 (Final Deliverable)

描述任务结束时的数据流向。
- **Save To**: `NAS/KnowledgeBase/Inbox`
- **Notify**: `Mobile` (If priority > high)

# 4. 异常处理 (Exception Handling)

- 如果 API 超时：Wait 5s and Retry (Max 3).
- 如果需要人工确认：Suspend and Send Check Card.
