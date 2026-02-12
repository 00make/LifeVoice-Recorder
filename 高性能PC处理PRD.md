# LifeOS Strategic Core PRD (Active Strategy Room Backend)

## 1. 产品名称

**LifeOS Strategic Core**（LifeOS 战略核心 / 主动战情室后端）

## 2. 产品目标

- **从“被动记录”转向“主动执行”**：不再是一个仅仅等待查询的数据库，而是一个会读取环境 context、主动匹配 SOP、并调度 Agent 执行任务的**战略指挥部**。
- **构建 Context-Awareness (场景感知能力)**：通过融合地理位置、生理状态、环境噪音等多模态数据，理解“此时此刻”的真实含义。
- **构建 SOP-Execution (SOP 执行能力)**：将模糊的 Intent 转化为精确的 Standard Operating Procedures (SOP)，并由 Agent Swarm 自动化执行。

## 3. 核心功能架构

### 3.1 洞察引擎 (Insight Engine & Context Fusion)

- **Context Fusion (情境融合)**：将单纯的 Audio (Text) 与 Sensor Data (Location, Heart Rate, App Usage) 结合。
  - *Example*: "I'm tired" (Audio) + Heart Rate > 110 (Sensor) = **High Stress Mode** (Trigger Recovery SOP).
- **Hidden State 提取**：提取潜台词与情绪状态，判断当前任务优先级。

### 3.2 战略匹配器 (Strategy Matcher)

- **SOP Retrieval**: 基于当前 Context 和 User Intent，从 `SOP Registry` 中检索最匹配的战术手册 (e.g., "紧急故障排查手册" vs "深度阅读模式").
- **Dynamic Prompting**: 将检索到的 SOP 注入到 Orchestrator 的 System Prompt 中。

### 3.3 战术编排器 (Tactical Orchestrator)

- **SOP Execution**: Orchestrator 严格按照 SOP 步骤拆解任务。
- **Agent Swarm Deployment**:
  - **Level 1 (Commander)**: 负责总体战略与 SOP 步骤监控。
  - **Level 2 (Specialist)**: 专职 Agent (Coder, Researcher, Writer) 并行工作。
- **Hybrid Logic**:
  - **Local**: 处理隐私数据与常规逻辑。
  - **Cloud (DeepSeek/GPT-4)**: 处理复杂推理与创意生成。

### 3.4 经验蒸馏 (Skill Distillation -> SOP)

- **Auto-SOP Generation**: 每次成功的任务执行后，Critic Agent 会复盘过程，生成或更新 `SKILL.MD` (标准作业程序)。
- **SOP Library**: 将个人隐性知识显性化，成为系统的“肌肉记忆”。

### 3.5 全景战略地图 (Strategic Knowledge Graph)

基于 **Input-Process-Output** 的动态战略地图。

- **Input Layer (感知)**:
  - **Context**: 物理/数字环境 (Where/When).
  - **State**: 生理/心理能量 (Energy Level).
- **Process Layer (战术)**:
  - **SOPs (Actions)**: **核心资产**。标准作业程序、Tool Chains、Agent Prompts。
  - **Strategies**: 针对特定 Context 的 SOP 组合。
- **Output Layer (战果)**:
  - **Assets**: 最终交付物 (代码、文章、视频)。
  - **Events**: 里程碑归档。

### 3.6 结果交付 (Result Delivery)

- **自动化执行**：直接调用 Tool 执行（如：发邮件、提交代码、控制家居）。
- **人机协同**：关键决策通过 Memos/Dashboard 请求 Commander (用户) 确认。

## 4. 非功能需求

- **并发处理**：支持同时运行 10+ 个 7B/8B 规模的 Agent。
- **响应速度**：Insight 阶段 < 30s，Simple Intent 执行 < 1min。
- **可观测性**：完整的 Agent 思考链（Chain of Thought）日志记录。

## 5. 风险与缓解

- **幻觉失控**：引入“对抗性进化”机制，设置专门的 Critic Agent 查错。
- **死循环**：Orchestrator 设置最大 Token 消耗与递归深度限制。
- **算力瓶颈**：动态量化（Dynamic Quantization），低优任务排队或卸载到 CPU。

## 6. 里程碑

- Phase 1：搭建 Local LLM (Ollama/vLLM) + 基础 RAG。
- Phase 2：实现 Single-Agent Loop (Insight -> Action)。
- Phase 3：实现 Multi-Agent Fission (动态生成子 Agent)。
