# LifeOS Command Deck PRD (Active Strategy Room UI)

## 1. 产品名称

**LifeOS Command Deck**（LifeOS 战略指挥舱 / 战情室 UI）

## 2. 产品目标

打造一个 **Total Information Awareness (全维信息感知)** 的战情室界面。
不仅是“回顾过去”，更是“指挥现在”和“规划未来”。
它是人类指挥官 (User) 观察 Swarm 运作、下达宏观指令的 **CIC (Combat Information Center)**。

## 3. 核心功能架构

### 3.1 战情总览 (Strategic Dashboard)

- **Situation Awareness (态势感知)**: 顶部状态栏显示 "Current Context" (e.g., "Deep Work Mode @ Home Office | Energy: High").
- **Operations Map (作战地图)**: 实时可视化的 Agent 活动热图。
- **Command Line**: 全局命令行，支持 Natural Language Commands (e.g., "部署 Project Alpha SOP").

### 3.2 洞察时间轴 (Intelligence Timeline)

- **Intelligence Report**: 每一条 Timeline Item 都是经过 Summarizer Agent 提炼的高价值情报，而非流水账。
- **Source Link**: 点击情报可追溯原始录音或 Context 数据。

### 3.3 全景资产流向图 (Strategic Ontology View)

从“静态档案博物馆”升级为“动态指挥中心”。不仅存储过去，更驱动未来。

#### 3.3.1 三大核心视图 (Strategy Views)

- **View A: 资源视图 (The Library View) - [Inventory]**
  - **内容**: 知识图谱 (Nodes)、SOP 库 (Manuals)、工具箱 (APIs)。
  - **用途**: 盘点资产。例如：查看 "我有哪些关于 Python 的 SOP?"
- **View B: 执行视图 (The Pipeline View) - [Operations]**
  - **内容**: 看板 (Kanban) / 甘特图 (Gantt)。
  - **用途**: 监控任务进度。显示 Agent 正在执行哪一步 SOP。
- **View C: 仪表盘视图 (The Dashboard View) - [Status]**
  - **内容**: 仪表盘 (Gauges)。精力水位、任务负载、系统健康度。
  - **用途**: 辅助决策。当精力水位低时，红色警报提示“建议休息”。

### 3.4 交互式指令台 (Direct Command Console)

- **Chat with Swarm**: 一个统一的对话框，可以 `@Recorder` 调取记忆，`@Coder` 写代码。
- **Approval Cards**: 关键决策的审批卡片（如：Agent 申请删除数据或发送邮件，需点击 [Approve]）。
  - **形态**：Kanban 或 动态流水线图。
  - **数据流**：`Input (Idea)` -> `Process (Action/SOP)` -> `Output (Asset)`.
  - **用途**：监控 Swarm 正在执行什么任务，哪里卡住了（缺少 SOP 或 Token 不足）。
- **View C: 决策视图 (The Dashboard View) - [规划]**
  - **形态**：仪表盘 + 能量槽。
  - **逻辑**：剩余精力 (State) vs 待办任务复杂度 (Actions)。
  - **用途**：判断今天剩余的“电量”还能处理几个复杂任务。

## 4. 界面隐喻


- **Sci-Fi Style**: 采用深色模式、单色荧光绿/橙配色，模拟专业控制台。
- **Density**: 高信息密度，一屏尽可能展示更多 Agent 状态。

## 5. 里程碑

- Phase 1: Memos 深度定制，增加 Agent 标签支持。
- Phase 2: 独立的 Commander Web UI，对接 LangSmith API 展示任务链。
- Phase 3: 移动端 Command App (Flutter)。
