# Ultimate LifeOS: The Active Strategy Room (ASR)

**LifeOS ASR** 是一个具备 **SOP 执行能力** 和 **场景感知能力** 的个人主动战情室。
它不再是一个被动的“录音笔/笔记软件”，而是一个 **永远在线的、主动为您运筹帷幄的数字参谋长**。

## 1. 核心定义 (The Shift)

从 **Archivist (档案员)** 进化为 **Strategist (战略家)**。

| 维度 | 旧 LifeOS (Passive) | 新 LifeOS ASR (Active) |
| :--- | :--- | :--- |
| **感知** | 记录声音 (Audio) | 感知语境 (Audio + Location + Biometrics) |
| **逻辑** | 检索信息 (Search) | 匹配 SOP (Strategy Matching) |
| **行动** | 等待查询 (Waiting) | 主动执行 (Execution) |
| **界面** | 笔记本 (List) | 战情室 (Dashboard) |

## 2. 系统架构 (The War Room Architecture)

### Layer 1: Field Sensors (前线感知)
- **LifeVoice Sensory (Android/Wear)**: 全天候采集声音，同时附带“地理位置”、“运动状态”、“生理指标”。
- **Context Fusion**: 将“我刚才说了什么”与“我在哪/我很累”结合，形成完整的 **Situation (态势)**。

### Layer 2: Strategic Core (战略核心 - PC/Brain)
- **Insight Engine**: 识别态势。识别出“这是一个灵感”还是“这是一个紧急BUG”。
- **SOP Registry (SOP 库)**: 存储您积累的所有技能说明书 (e.g., "如何写周报", "如何处理服务器报警").
- **Strategy Matcher**: 自动将 **Situation** 映射到对应的 **SOP**。

### Layer 3: Tactical Swarm (战术集群 - Agents)
- **Orchestrator**: 指挥官 Agent，负责拆解 SOP。
- **Special Forces**: 专职 Agent (Coder, Writer, Analyst) 并行执行任务。
- **Tools**: 调用 API, CLI, IoT 接口。

### Layer 4: Command Deck (指挥舱 - Visualization)
- **Library View**: 资源与知识图谱 (Past).
- **Pipeline View**: 正在执行的任务流水线 (Present).
- **Dashboard View**: 精力水位与决策建议 (Future).

## 3. 核心数据流 (The Strategic Loop)

1.  **Sense**: 也是感知。Sensor 捕捉到您在 *Starbucks* 说 "Start Project X"。
2.  **Contextualize**: 系统识别到 Location=Starbucks (Work Mode), State=High Energy.
3.  **Decide**: 检索 SOP 库，找到 `SOP_Project_Kickoff.md`。
4.  **Exchange**: Orchestrator 激活 Product Manager Agent & Tech Lead Agent。
5.  **Act**: Agents 自动创建 GitHub Repo，生成 Notion Page，发送 Slack 通知。
6.  **Report**: 指挥舱即时显示 "Project X Kickoff: 25% Active".

## 4. 落地路线

- **Phase 1: Awareness (感知)** - 建立 Context Node，让系统知道你在哪、状态如何。
- **Phase 2: Procedure (规程)** - 沉淀 `SKILL.MD`，建立 SOP 库。
- **Phase 3: Execution (执行)** - 让 Agent 能够读取 SOP 并调用 Tools。
- **Phase 4: Synthesis (全知)** - 完整的战情室视图。


为保证可执行性，拆分为多个 PRD 与开发实践指南：

- 手机端录音：
  - `Android端录音模块PRD.md`
  - `Android端录音模块开发实践指南.md`
- NAS 存储/传输：
  - `NAS端存储与传输PRD.md`
  - `NAS端存储与传输开发实践指南.md`
- 高性能 PC 处理：
  - `高性能PC处理PRD.md`
  - `高性能PC处理开发实践指南.md`
- 实时传感器采集（手机/手表/边缘设备）：
  - `实时传感器采集PRD.md`
  - `实时传感器采集开发实践指南.md`
- 多 Agent 处理与调度：
  - `多Agent处理与调度PRD.md`
  - `多Agent处理与调度开发实践指南.md`
- 反馈与行动（推送/语音播报）：
  - `反馈与行动PRD.md`
  - `反馈与行动开发实践指南.md`
- 闭环学习（LoRA/持续学习）：
  - `闭环学习PRD.md`
  - `闭环学习开发实践指南.md`

## 4. 数据流闭环（Swarm Loop）

1.  **Insight (洞察)**：采集层上传数据，Insight Agent 识别出“用户需要X”。
2.  **Intent (意图)**：Master Agent 将需求转化为“任务书”与 KPI。
3.  **Fission (裂变)**：Orchestrator 生成 N 个 Expert Agents 并行执行（搜索、编码、分析）。
4.  **Result (结果)**：Critic Agent 验收成果，最终交付给 Commander (用户) 或写入长期记忆。

## 5. 里程碑（可执行版本）

- Phase 1（0-6 个月）：**感知构建**。录音采集 + NAS 存储 + 基础转录 + RAG 知识库搭建。
- Phase 2（6-12 个月）：**意图理解**。多模态融合 + 基础 Agent 调度 (LangGraph/AutoGen) + 自动化任务执行。
- Phase 3（12-24 个月）：**群体智能**。实现 `Insight -> Intent -> Fission` 全自动闭环，达到“一人即军团”状态。

## 6. 约束与原则

- **算力即正义**：充分压榨本地 GPU (RTX 4090/5090) 性能，减少云端依赖。
- **Agent 可观测性**：必须记录每个 Agent 的思考过程 (CoT) 与决策树。
