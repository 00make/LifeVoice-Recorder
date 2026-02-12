# LifeOS Strategic Graph Schema (Neo4j / PostgreSQL Topology)

## 1. 核心设计理念

从“平面流水账”升级为 **“立体作战地图” (Knowledge Graph)**。
虽然底层可能仍使用 PostgreSQL (`jsonb`) 存储元数据，但逻辑层必须按照图数据库 (Neo4j) 的节点与边来设计，以支持复杂的 **多跳推理 (Multi-hop Reasoning)** 和 **SOP 匹配**。

## 2. 图谱节点定义 (Graph Nodes)

### Layer 1: Input (感知层)

- **`Context` (情境)**
  - *Properties*: `{ type: "location|virtual", name: "Starbucks", coords: "...", wifi_ssid: "..." }`
  - *Usage*: 触发特定 SOP 的环境锚点。
- **`State` (状态)**
  - *Properties*: `{ type: "bio|psych", name: "HighEnergy", value: 0.9, timestamp: "..." }`
  - *Usage*: 决定 Agent 介入的激进程度。
- **`Person` (人物)**
  - *Properties*: `{ name: "Alice", relation: "Colleague", importance: 0.8 }`

### Layer 2: Process (战术层)

- **`Idea` (灵感/原始意图)**
  - *Properties*: `{ content: "Start a podcast", source_audio_id: "...", status: "pending" }`
- **`SOP` (战术手册)**
  - *Properties*: `{ name: "Podcast Production Workflow", trigger_condition: "Context.name='Studio' AND Idea.topic='Tech'", steps: [] }`
  - *Content*: 存储具体的 Markdown 流程和 Agent Prompt 模板。
- **`Task` (具体任务)**
  - *Properties*: `{ sop_id: "...", assigned_agent: "EditorAgent", status: "running" }`

### Layer 3: Output (资产层)

- **`Asset` (数字资产)**
  - *Properties*: `{ type: "file|code|link", path: "nas://...", summary: "..." }`
- **`Event` (记忆事件)**
  - *Properties*: `{ type: "meeting|milestone", date: "...", participants: [] }`

## 3. 图谱关系定义 (Relationships)

### 动态触发流程
- `(User)-[LOCATED_AT {time: ...}]->(Context)`
- `(Context)-[TRIGGERS {probability: 0.9}]->(SOP)`  <-- **核心: 场景触发SOP**
- `(State)-[MODULATES]->(SOP)` (e.g., 疲劳状态降低 Coding SOP 的优先级)

### 任务执行流程
- `(Idea)-[MATCHES]->(SOP)`
- `(SOP)-[SPAWNS]->(AgentTeam)`
- `(Agent)-[PRODUCES]->(Asset)`

## 4. 物理表结构 (PostgreSQL Implementation Draft)

虽然逻辑是图，但物理存储推荐 Hybird (PG + Vector)。

### 4.1 `nodes` table (通用节点表)
```sql
CREATE TABLE nodes (
    id UUID PRIMARY KEY,
    label TEXT NOT NULL, -- 'SOP', 'Context', 'Idea'
    properties JSONB,    -- Flexible schema
    embedding VECTOR(1536) -- For semantic search
);
```

### 4.2 `edges` table (通用边表)
```sql
CREATE TABLE edges (
    source_id UUID REFERENCES nodes(id),
    target_id UUID REFERENCES nodes(id),
    relation_type TEXT, -- 'TRIGGERS', 'PRODUCES'
    properties JSONB,
    PRIMARY KEY (source_id, target_id, relation_type)
);
```

### 4.3 `sop_registry` table (SOP 专用存储)
```sql
CREATE TABLE sop_registry (
    sop_id UUID PRIMARY KEY,
    name TEXT,
    content_markdown TEXT, -- 完整的 .md 文件内容
    required_capabilities TEXT[], -- ['internet', 'python']
    version INT
);
```
