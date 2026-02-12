# NAS Memory Lake 开发实践 Guide

本指南聚焦如何将 NAS 改造为 Agent Swarm 的 **高吞吐数据总线** 与 **持久化记忆库**。

## 1. 核心容器栈 (Docker Compose)

```yaml
services:
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
  
  postgres:
    image: pgvector/pgvector:pg16  # 支持向量插件
    volumes:
      - ./pgdata:/var/lib/postgresql/data

  chroma:
    image: chromadb/chroma
    ports:
      - "8000:8000"
      
  redis:
    image: redis:alpine
    # 作为 Event Bus
```

## 2. 数据目录规范 (The Memory Structure)

- `s3://sensory-raw/` (Immutable): 存放 Edge 上传的原始加密数据。
- `s3://long-term-mem/`: 存放经过清洗的 Markdown/JSON 知识库。
- `s3://swarm-logs/`: 存放 Agent 的完整思考过程日志。

## 3. 关键服务逻辑

### 3.1 智能触发器 (Smart Trigger)

不再是简单的 Webhook，而是一个运行在 NAS 上的轻量脚本 (Python/Go)：
1. 监听 MinIO Bucket Notification。
2. 读取文件 Metadata (如 `intent:command`)。
3. 如果是 Command，直接向 PC 发送 `Wake-on-LAN` 并推送高优先级消息。
4. 如果是 Routine，仅推送到 Redis 做 Batch 处理。

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
