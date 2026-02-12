# LifeOS Tactical Orchestration Implementation Guide (Active Strategy Room)

本指南聚焦于如何实现 **SOP-based Execution Swarm**，核心是让 Agent 严格遵循 **Standard Operating Procedures (SOP)** 进行战斗。

## 1. 技术栈选型 (Tactical Stack)

- **Orchestration Core**：
  - **LangGraph**: 唯一推荐。完美契合 State Machine + Graph 拓扑，能够精确实现 SOP 中的 "Step 1 -> Step 2 -> Checkpoint" 逻辑。
  - **Implementation**: 见 `brain/sop_engine.py`。
- **SOP Format**: `Markdown` (人类可读) + `YAML Frontmatter` (机器可解析元数据)。
- **Trigger System**:
  - **Context Watcher**: 见 `brain/context_watcher.py`，负责监听传感器数据并激活 SOP。
- **Prompt Engineering**:
  - **System Prompt Injection**: 将 SOP 的当前步骤作为 System Prompt 动态注入给 Worker。

## 2. 核心模式实现 (Patterns)

### 2.1 模式一：SOP 加载与执行 (The SOP Engine)

将 Markdown 格式的 SOP 转换为 LangGraph 的 `StateGraph`。

```python
# 核心逻辑 (见 brain/sop_engine.py)
class SOPEngine:
    def _parse_sop_md(self, path):
        # Parses YAML Frontmatter + Markdown Steps
        ...
        
    def _build_graph(self):
        # Maps SOP Steps -> LangGraph Nodes
        workflow = StateGraph(AgentState)
        for step in self.sop.steps:
            workflow.add_node(step.name, ...)
        return workflow.compile()
```

### 2.2 模式二：动态路由 (Context-Aware Routing)

由 `ContextManager` (The Eye) 负责感知环境变化并推送 Trigger 信号。

```python
# 见 brain/context_watcher.py
async def evaluate_triggers(self, context_payload):
    # Rule 1: Morning Briefing
    if context.location == "Home" and context.activity == "WakingUp":
        return ["SOP_001_Morning_Briefing"]
    
    # Rule 2: Stress Intervention
    if context.biometrics.stress == "High":
        return ["SOP_999_Emergency_Calm"]
```

## 3. SOP 文档结构规范 (SOP Spec)

一个标准的 SOP `.md` 文件应包含 YAML 头和步骤定义：

```markdown
---
id: SOP_001_Morning_Briefing
alias: "Golden Morning"
trigger:
  - "Condition: Location == Home AND State == WakingUp"
roles: 
  - { id: "analyst", model: "deepseek-v3" }
  - { id: "writer", model: "qwen2.5-14b" }
---

# Phase 1: Context Gathering
- **Step 1.1**: Query `CalendarAPI` for priorities.

# Phase 2: Action
- **Step 2.1**: Synthesize briefing audio.
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
