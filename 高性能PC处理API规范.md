# LifeOS Control Plane API Specs

本规范定义了主机侧与外界（Android Sensor, Commander Deck, SOP Tools）交互的核心 API。

## 1. Context Ingestion (感知接入)

### POST `/ingest/context`

- **Purpose**: 更新系统的"当前态势" (Current Situation).
- **Source**: Android Sensor, Wear OS, Desktop Watcher.

### 请求体

```json
{
  "timestamp": "2026-02-12T12:00:00Z",
  "source_device": "pixel_9",
  "context_nodes": [
    {
      "type": "LOCATION",
      "value": "Home Office",
      "confidence": 0.95
    },
    {
      "type": "ACTIVITY",
      "value": "Working",
      "metadata": { "app": "VSCode", "focus_score": 85 }
    },
    {
      "type": "BIO_STATE",
      "value": "High Energy",
      "metadata": { "hr": 75, "stress": 12 }
    }
  ]
}
```

### 响应

```json
{
  "status": "updated",
  "triggered_sops": ["sop_deep_work_monitor"] // Return any immediate actions triggered
}
```

## 2. SOP Management (战术管理)

### POST `/sop/upload`

- **Purpose**: 上传或更新一个 Markdown 格式的 SOP。

### 请求体 (Multipart)

- `file`: `SOP_name.md`
- `metadata`: `{"tags": ["coding", "python"], "min_energy_level": "medium"}`

### GET `/sop/list`

- **Purpose**: 获取当前可用的 SOP 列表。
- **Response**: `[{"id": "sop_001", "name": "Python Crawler", "usage_count": 12}]`

## 3. Operations Graph (作战地图)

### GET `/graph/active`

- **Purpose**: 获取当前正在运行的 Agent 任务及其所属的 Context/SOP，用于可视化层绘制 "Pipeline View"。

### 响应

```json
{
  "nodes": [
    { "id": "task_123", "type": "TASK", "label": "Crawling GitHub", "status": "running" },
    { "id": "agent_coder", "type": "AGENT", "label": "Coder-01" },
    { "id": "sop_crawler", "type": "SOP", "label": "Universal Crawler" }
  ],
  "edges": [
    { "source": "sop_crawler", "target": "task_123", "rel": "SPAWNED" },
    { "source": "task_123", "target": "agent_coder", "rel": "ASSIGNED_TO" }
  ]
}
```

## 4. Legacy Endpoints (保留)

### POST `/webhook/nas/object-created` (No Change)
### GET `/tasks/{task_id}` (No Change)
