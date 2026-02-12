# LifeOS S-Evol PRD (Self-Evolving SOP Engine)

## 1. 产品名称

**LifeOS Evolution Engine**（群体智能进化引擎 / SOP 蒸馏器）

## 2. 产品目标

核心目标：**Turn Experience into Strategy (将经验转化为战略)**。
不仅仅是数据积累，而是 **Cognitive Architecture** 的自我迭代。
核心手段是从成功的交互中 **蒸馏 (Distill)** 出新的 `SKILL.MD` (SOP)，并持续优化现有的 SOP。

## 3. 核心功能架构

### 3.1 经验蒸馏 (Skill Distillation -> Create SOP)

- **Post-Action Review (复盘)**: 每次 Task 成功关闭后，`Distiller Agent` 自动介入。
- **Conversion**: 将对话历史 (Chat History) 和 代码片段 (Snippets) 转化为标准化的 Markdown SOP。
  - *Input*: "帮我把这两个 PDF 里的表格提取出来合并成 Excel。" -> *Execution* ... -> *Success*.
  - *Output*: 生成 `SOP_PDF_Table_Extraction.md`，包含使用的库 `PyPDF2` 和处理逻辑。

### 3.2 战略优化 (Strategy Optimization -> Update SOP)

- **DSPy Optimizer**: 监控 SOP 执行的成功率。
  - 如果某一步骤经常报错 (Error Rate > 20%)，自动修改 SOP 中的 Prompt 或尝试新的工具。
- **A/B Testing**: 针对频次极高的任务，生成变体 SOP (Variant A/B)，保留效率更高的版本。

### 3.3 记忆固化 (Memory Consolidation)

- **Nightly Routine (夜间整理)**: 类似于人类做梦。每天凌晨 3 点，Evolution Engine 唤醒。
- **Graph Updates**: 将新生成的 SOP 节点挂载到 Knowledge Graph 的正确位置 (e.g., 关联到 `tag:OfficeWork`)。
- **Vector Indexing**: 更新 SOP 的向量索引，方便 Strategy Matcher 检索。

### 3.4 风格克隆 (Style LoRA)

- **Objective**: 让 Agent 的 Writer 分身学习用户的写作风格。
- **Data Source**: 用户的历史日记、博客、微信聊天记录。
- **Action**: 每周触发一次 Unsloth LoRA Fine-tuning，更新 `adapter_style.safetensors`。

## 4. 进化机制

- **Survival of the Fittest**: 统计哪些 Tool 和 SOP 被频繁使用且成功率高，提升其在检索时的权重；淘汰长期不用的“僵尸技能”。

## 5. 里程碑

- Phase 1: **Manual Distillation**. 提供 CLI 工具手动将 Session 转为 MD。
- Phase 2: **Auto-SOP**. 简单的模板填充式自动生成。
- Phase 3: **Self-Healing SOP**. 基于执行报错自动修正 SOP 代码块。
