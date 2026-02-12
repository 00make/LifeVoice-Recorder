# LifeOS Tactical Operations PRD (SOP Execution Swarm)

## 1. 产品名称

**LifeOS Tactical Operations Center**（LifeOS 战术行动中心 / SOP 执行集群）

## 2. 产品目标

核心目标：**SOP Deployment & Execution (标准作业程序部署与执行)**。
系统不再仅仅是根据意图“动态裂变”，而是 **严格执行战略层下发的 SOP**，确保每一次行动都符合最佳实践。
从“自由发挥”进化为“训练有素的特种部队”。

## 3. 核心功能架构

### 3.1 战术分组 (Tactical Squads)

- **Context Sentinel (哨兵)**：
  - **职责**：7x24h 监控 Context Stream (传感器数据流)。
  - **触发**：一旦发现 Condition Matches (e.g., "User enters Deep Work Mode"), 立即激活对应的 SOP。
- **SOP Librarian (图书管理员)**：
  - **职责**：维护 `SOP Registry`。接收战略层的指令，取出正确的战术手册 (Markdown)。
  - **注入**：将 SOP 中的步骤注入到 Worker Agent 的 System Prompt 中。
- **Field Operators (外勤特工)**：
  - **Writer / Coder / Analyst**：根据 SOP 执行具体任务的 Worker Agent。
  - **Tools**: 为 Agent 配备具体的 API 访问权 (Gmail, Notion, GitHub)。

### 3.2 SOP 执行引擎 (SOP Execution Engine)

- **Step-by-Step Execution**: 严格遵循 SOP 中的步骤 (Step 1, Step 2, Checkpoint)。
- **Compliance Check**: 每一步骤执行后，Critic Agent 需对照 SOP 标准进行验收。
- **Exception Handling**: 遇到 SOP 未覆盖的情况，上报给 Strategy Core 请求新指令。

### 3.3 对抗性进化网络 (Adversarial Optimization)

- **Red Team (Executors)**：执行任务，生成结果。
- **Blue Team (Critics)**：对照 SOP 标准进行质检。
  - *Example*: SOP 要求 "代码必须包含单元测试"，如果 Executor 没有生成测试，Critic 直接驳回。

### 3.4 动态资源调度 (Shared Blackboard & Resources)

- **Shared Memory**: 所有 Agent 通过 Redis/VectorDB 共享短期记忆，确保信息同步。
- **Budgeting**: 根据任务优先级 (来自 Context State)，动态分配 Token 预算和算力资源。
- **Parallelism**: 对于并行步骤 (e.g., "同时搜索 Google 和 GitHub"), 自动裂变多个 Worker 并行处理。

### 3.5 人类介入协议 (Human-in-the-Loop)

- **Confirm Card**: 当 Critic Agent 发现所有方案均未达标，或涉及高危操作 (Delete/Purchase) 时，主动挂起任务链，向 Commander (用户) 发送确认请求。

## 4. 非功能需求

- **Reliability**: SOP 执行成功率 > 95%。
- **Latency**: 哨兵触发响应时间 < 2s。
- **Traceability**: 全程记录 SOP 执行日志，供战略层复盘。
- **Cost / Token Control**：设置单次任务的最大 Token 预算，防止无限递归。

## 5. 里程碑

- Phase 1：**Static SOP Execution**。手动定义的 LangGraph 工作流 (固定 SOP)。
- Phase 2：**Dynamic SOP Loading**。Orchestrator 可以根据 Context 动态加载不同的 `SOP_*.md`。
- Phase 3：**Autonomous SOP Optimization**。Agent 团队能够自我复盘，将执行中的改进点写回 `SOP Registry`。

