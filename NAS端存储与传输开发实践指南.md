# NAS Memory Lake 开发实践 Guide

本指南聚焦如何将 NAS 改造为 Agent Swarm 的 **高吞吐数据总线** 与 **冷存储记忆库**。
*注意：高性能向量计算 (Vector DB) 和 图计算 (Neo4j) 建议运行在算力节点 (Compute Node/PC)，NAS 主要负责大容量对象存储。*

## 1. 核心容器栈 (Docker Compose)

```yaml
services:
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
  
  postgres:
    # 仅作为冷备份或结构化日志存储
    image: postgres:16
    volumes:
      - ./pgdata:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    # 作为跨设备 Event Bus (Sensors -> NAS -> PC)
```

## 2. 数据目录规范 (The Memory Structure)

- `s3://sensory-raw/` (Immutable): 存放 Edge 上传的原始加密数据 (Audio/Video).
  - 路径格式: `date/device_id/timestamp.opus`
- `s3://knowledge-base/`: 存放 SOP 和 Wiki 的 Markdown 备份.
- `s3://swarm-logs/`: 存放 Agent 的完整思考过程日志 (Archival for Distillation).

## 3. 关键服务逻辑

### 3.1 智能触发器 (Smart Trigger)

一个运行在 NAS 上的轻量脚本 (Python/Go)：
1. 监听 MinIO Bucket Notification (e.g., New Audio Uploaded).
2. 判断优先级：
   - 包含 `intent` 标记 -> 立即通过 webhook 通知 PC 端的 `api_server.py`.
   - 普通日志 -> 仅归档。

### 3.2 向量化流水线 (如果 NAS 性能允许)

*可选：如果 NAS 是高性能型号（如 i5-12400+），可分担 part of core work。*
- 当新文档写入，NAS 自动调用本地 embedding 模型（如 `all-MiniLM-L6-v2`）生成向量并存入 Chroma。
- 减轻 Core PC 的负担。

## 4. 安全加固

- **Internal Only**: ChromaDB 和 Redis 仅监听内部 Docker Network 或 WireGuard 接口，严禁暴露公网。
- **Audit Log**: 记录哪一个 Agent (AgentID) 在什么时间访问了哪一段记忆。

## 5. 运维监控

- 监控 ChromaDB 的索引体积与检索延迟。
- 监控 MinIO 的吞吐量，确保 Sensor 上传不积压。
