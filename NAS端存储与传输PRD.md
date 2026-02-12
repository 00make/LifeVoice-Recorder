# NAS 端存储与传输 PRD (Memory Lake Protocol)

## 1. 产品名称

**LifeOS Memory Lake**（Swarm 共享数据湖 / 战术资源库）

## 2. 产品目标

不仅是文件存储，而是 Agent Swarm 的 **Shared Long-Term Memory (共享长期记忆)** 和 **SOP Registry (SOP 仓库)**。
它是连接 Edge (Sensory) 与 Core (Brain) 的海马体 (Hippocampus)，同时也是存放“战术手册”的图书馆。

## 3. 核心功能架构

### 3.1 统一感知接入 (Universal Sensory Ingest)

- **Input Types**: 接收 Audio, Image, Logs, Sensor JSON 等全模态数据。
- **Immutable Ledger**: 像区块链一样记录所有原始数据，不允许篡改，只允许追加 (Append-only)。

### 3.2 战术资源库 (Strategic Assets Storage)

- **Vector Memory Bank**: 存储 Embeddings (Chroma/Milvus)，供 RAG 检索。
- **SOP Registry**: 专门的 bucket (`s3://lifeos-sops/`) 存储所有 `SKILL.MD` 文件。
  - **Versioning**: 支持 S3 Versioning，记录 SOP 的每一次迭代。

### 3.3 信号中继 (Signal Relay)

- **Tactical Path (Fast)**: 对于 `intent:command` 的上传（如“开始工作”），直接触发 Webhook 唤醒 PC 端的 Orchestrator。
- **Archival Path (Slow)**: 对于 `type:background` 的背景录音，仅进行存储和异步索引，不触发 Agent。

### 3.4 隐私保险箱 (Privacy Vault)

- 所有敏感数据（语音、日记）在 NAS 落地即加密 (Encryption at Rest)。
- Agent 只有在获得 Authorization Token 后才能解密读取特定 Context。

## 4. 技术架构调整

- **Storage Layer**: MinIO (Blob) + PostgreSQL (Meta) + **ChromaDB (Vector)**.
- **Message Bus**: Redis (Task Queue) / MQTT (Sensor Stream).

## 5. 里程碑

- Phase 1: 基础文件存储 (MinIO).
- Phase 2: 事件总线与 Webhook (Redis).
- Phase 3: **SOP 专用 Git 仓库集成** (在 NAS 上运行 Gitea 托管 SOP 版本历史)。
