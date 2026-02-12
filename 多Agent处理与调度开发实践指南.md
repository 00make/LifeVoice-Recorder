# LifeOS Tactical Orchestration Implementation Guide

本指南聚焦于如何实现 **SOP-based Execution Swarm**，核心是让 Agent 严格遵循 **Standard Operating Procedures (SOP)** 进行战斗。

## 1. 技术栈选型 (Tactical Stack)

- **Orchestration Core**：
  - **LangGraph**: 唯一推荐。完美契合 State Machine + Graph 拓扑，能够精确实现 SOP 中的 "Step 1 -> Step 2 -> Checkpoint" 逻辑。
- **SOP Format**: `Markdown` (人类可读) + `YAML Frontmatter` (机器可解析元数据)。
- **Prompt Engineering**:
  - **System Prompt Injection**: 将 SOP 的当前步骤作为 System Prompt 动态注入给 Worker。

## 2. 核心模式实现 (Patterns)

### 2.1 模式一：SOP 加载与执行 (The SOP Runner)

将 Markdown 格式的 SOP 转换为 LangGraph 的 `StateGraph`。

```python
# 伪代码：SOP 到 Graph 的转换
def load_sop_to_graph(sop_path):
    sop = parse_markdown(sop_path) # 解析出 steps
    workflow = StateGraph(AgentState)
    
    # 1. Add Nodes
    for step in sop.steps:
        # 为每个步骤创建一个 Node
        workflow.add_node(step.id, create_agent_node(role=step.role, prompt=step.instruction))
        
    # 2. Add Edges (Linear or Branching)
    for i in range(len(sop.steps) - 1):
        workflow.add_edge(sop.steps[i].id, sop.steps[i+1].id)
        
    # 3. Add Checkpoints (Human-in-the-loop)
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
```

### 2.2 模式二：动态路由 (Context-Aware Routing)

```python
def router_node(state):
    # 根据 Context 决定加载哪个 SOP
    context = state['context']
    if context.location == "Gym":
        return "sop_fitness_log"
    elif context.idea_type == "coding":
        return "sop_github_pr"
    else:
        return "sop_general_chat"
```

## 3. SOP 文档结构规范 (SOP Spec)

一个标准的 SOP `.md` 文件应包含：

```markdown
---
id: sop_daily_report
trigger: "Timer: 18:00" OR "Intent: Summarize today"
roles: [Summarizer, Formatter]
---

# Daily Report Protocol

## Step 1: Gather Data (Summarizer)
- Action: RAG Query "What did I do today?"
- Output: Raw Bullet Points.

## Step 2: Format (Formatter)
- Action: Transform to Markdown Table.
- Checkpoint: Human Approval needed before Save.
```

## 4. 调试与追踪

- **LangSmith**: 必须配置。用于追踪具体的 Step 执行耗时和 Token 消耗。
- **State Rewind**: 利用 LangGraph 的 Checkpointer 功能，当 SOP 执行失败时，"倒带"回上一步并重试。
        
```python
    return sub_graph.compile().invoke(state)
```

## 4. 调试与追踪

- **LangSmith**: 必须配置。用于追踪具体的 Step 执行耗时和 Token 消耗。
- **State Rewind**: 利用 LangGraph 的 Checkpointer 功能，当 SOP 执行失败时，"倒带"回上一步并重试。

### 2.2 模式二 (Legacy): 评审团机制 (The Jury)
*注：此模式主要用于 Creative Writing 任务，不用于标准 SOP 执行。*

## 5. 调试与安全 (Safety Rails)

- **Recursion Limit**: 必须设置 Graph 的 `recursion_limit=20`，防止 Agent 无限相互指派任务。
- **Budget Control**: 可以在 Context 中注入 `remaining_budget` 变量，每调用一次 LLM 扣除相应 Token 额度，归零则强制终止。

## 5. 最佳实践

- **Prompt as Code**: 所有 Agent 的 System Prompt 必须版本化 (Git)。
- **Unit Test for Agents**: 准备这套 Golden Dataset (输入->理想输出)，每次修改 Prompt 后跑回归测试。
