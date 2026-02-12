# LifeOS Strategic Core Implementation Guide (Active Strategy Room)

本指南覆盖主机侧从“数据处理”向“群体智能战情室”转型的完整实现流程。
核心任务：构建 **Context-Aware Triggering System (情境触发系统)** 和 **SOP Execution Engine (SOP 执行引擎)**。

## 1. 基础设施栈 (Infrastructure Stack)

- **Compute**: Windows 11 (WSL2) + Dual RTX 4090 (NVLink).
- **LLM Runtime**:
  - `vLLM`: High-throughput serving for 7B/14B quantized models (Mistral, Qwen).
  - `Ollama`: Local embeddings and small utility models.
- **Graph Database**: `Neo4j` (Community Edition). Stores the **Strategic Graph** (Nodes: Context, SOP, Action).
- **Vector Database**: `ChromaDB` (Persistent Mode). Stores `SOP` embeddings and `Memory` clusters.
- **Orchestration**: `LangGraph`. stateful multi-agent workflows.

## 2. 核心模块实现 (Core Implementation)

### 2.1 The Graph Topology (Neo4j Setup)

使用 `neo4j-driver` Python 库构建动态关系。

```python
# Example: Creating a Context Trigger
def register_context_trigger(context_name, sop_id, probability=1.0):
    query = """
    MATCH (c:Context {name: $context_name})
    MATCH (s:SOP {id: $sop_id})
    MERGE (c)-[:TRIGGERS {prob: $prob}]->(s)
    """
    session.run(query, context_name=context_name, sop_id=sop_id, prob=probability)
```

### 2.2 The Strategy Matcher (Context -> SOP)

**逻辑**: 当 Context 发生变化时，查询 Graph 寻找被激活的节点。

- **Input**: `Context Vector` (e.g., `[Location=Home, Time=22:00, Energy=Low]`).
- **Query**:
  1.  Find active `Context` nodes.
  2.  Traverse `[:TRIGGERS]` edges.
  3.  Filter by `State` (e.g., if Energy < 0.3, ignore "Coding" SOPs).
  4.  Return candidate `SOP List`.

### 2.3 The SOP Execution Engine (LangGraph)

**结构**: 每个 SOP 是一个 Graph, 每个 Step 是一个 Node.

- **SOP Loader**: 解析 Markdown 文件 (见 `brain/sop_engine.py`)。
- **Dynamic Graph Construction**:
  ```python
  # (See implementation in brain/sop_engine.py)
  workflow = StateGraph(AgentState)
  for step in self.sop.steps:
      workflow.add_node(step.name, self._create_node_function(step))
  ```

### 2.4 Hybrid Router (Local vs Cloud)

- **Rule-based Routing**:
  s- `config/config.yaml` 定义了不同 Agent Role 对应的 Model Provider。
  - `analyst` -> `DeepSeek-V3` (Cloud).
  - `writer` -> `Qwen-2.5-14B` (Local).

## 3. 开发路线图 (Current Status)

### Phase 1: The Base (Memory & Graph)
- [x] 部署 Neo4j 与 ChromaDB (Configuration in `config/config.yaml`).
- [x] 定义基础 Schema与操作 (Reference `knowledge_graph/graph_client.py`).

### Phase 2: The Eye (Context Ingestion)
- [x] 实现 `POST /ingest/context` 接口 (Reference `gateway/api_server.py`).
- [x] 编写规则引擎：`brain/context_watcher.py` (Implements `evaluate_triggers`).

### Phase 3: The Brain (SOP Engine)
- [x] 编写 `SOP Parser`：(Reference `brain/sop_engine.py`).
- [x] 搭建 `LangGraph` 运行环境：已实现基础 `SOPEngine` 类。

### Phase 4: The Interface (Commander Deck)
- [ ] 暴露 `GET /graph/active` 接口 (Stub implemented in `api_server.py`).
- [ ] 前端可视化开发 (Next.js + ForceGraph).


### 3.2 任务编排建议

- **小模型，大群体**：对于 Worker Agents，优先使用量化后的 7B/8B 模型 (Llama-3, Qwen-2.5) 以最大化并发。
- **大模型，做决策**：Master/Orchestrator Agent 使用 70B+ 或 GPT-4/Claude-3.5 级别模型 (API 或 本地量化) 以保证逻辑正确。

## 4. 关键实现要点

- **Agent 记忆设计**：
    - Short-term: 当前对话 Context Window。
    - Long-term: 写入 Vector DB 的总结与事实。
- **Tool Use 安全**：
    - 敏感操作 (如删除文件、对外发送) 必须经过 Human-in-the-loop 确认。
    - 代码执行必须在隔离沙箱 (Docker Container) 中进行。

### 4.1 观测与调试

- 集成 **LangSmith** 或 **Arize Phoenix** 追踪 Agent 的每一次调用与 Token 消耗。
- 记录 Agent 之间的 "对话日志" 以优化 Prompt。

### 4.2 失败与自愈

- **Re-planning**: 如果 Worker 连续 3 次失败，Manager 应当重新规划任务路径，而不是单纯重试。
- **Human Handoff**: 遇到无法解决的 Deadlock，主动向用户手机推送求助通知。

## 5. 测试与验证

- **图灵测试变体**：Agent 生成的摘要/代码是否不仅“正确”，而且符合用户的“风格” (Style Transfer)。
- **压力测试**：同时并发 20 个 Agent 交互，检测 vLLM 的吞吐量与显存稳定性。
### 5.2 指标建议

- 端到端处理耗时
- ASR 字错误率（抽样）
- 失败重试率

## 6. 运维建议

- 每日处理报告（耗时/失败率）
- 模型版本灰度与回滚
- 定期清理中间文件

### 6.1 日志与追踪

- 统一 trace_id 贯穿 ingest → writeback
- 每个任务记录输入 hash 与输出 hash

### 6.2 安全建议

- 解密只在内存进行
- 训练数据与处理数据隔离存储
