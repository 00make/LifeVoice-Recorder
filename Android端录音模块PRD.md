# LifeOS Field Sensor PRD (Active Sensory Node)

## 1. 产品名称

**LifeOS Field Sensor**（LifeOS 前线感知节点 / 听觉与环境传感器）

## 2. 产品目标

核心目标：**Situational Awareness (态势感知)**。
不再仅仅是录音机，而是个人战情室的 **前线侦察兵 (Scout)**。
它负责全天候捕捉用户的“指令”、“对话”与“环境声”，并融合传感器数据，为战情室提供 **Context**。

**核心理念升级**：
- **Context is King**：不仅仅录声音，通过 Sensor 融合（位置/运动/屏幕状态）提供“语境”。
- **Intent Trigger**：支持通过关键词（“Jarvis...”）或物理按键，向 Swarm 发送高优先级 **Tactical Intent**。

## 3. 目标用户

- **LifeOS指挥官**：需要随时向背后的 Agent 军团下达指令的人。

## 4. 核心功能架构

### 4.1 智能听觉感知 (Auditory Intelligence)

- **VAD 2.0 (Voice Activity Detection)**：区分“有效对话”与“背景噪音”，仅上传有价值的信息片段。
- **Speaker ID（端侧）**：初步标记“Commander Voice”和其他人声，确保只响应指挥官指令。

### 4.2 意图触发 (Tactical Intent Injection)

- **Wake Word**: 检测到 "Hey LifeOS" 或自定义词，立即以此为时间戳标记 `Action Trigger`。
- **Quick Action**: 通知栏快捷按钮 "Log Idea" / "Start Focus Mode"，直接向战情室发送状态变更信号。

### 4.3 多模态上下文融合 (Context Fusion)

- 每一段录音必须附带 **Sidecar Metadata (元数据侧车)**：
  - **Location**: GPS / Wi-Fi SSID (e.g., "Home", "Office", "Commute").
  - **Motion**: Accelerometer (e.g., "Walking", "Driving", "Stationary").
  - **Device State**: Screen On/Off, Battery Level.

### 4.4 安全战术上传 (Secure Tactical Uplink)

- **Priority Queue**: 对于 `intent:command` 或 `alert:high` 的数据，走即时蜂窝通道上传。
- **Bulk Upload**: 对于常规背景录音，走 Wi-Fi 批量同步至 NAS 记忆湖。

### 4.5 实时转录 (Live Insight)

- 端侧运行 sherpa-onnx (SenseVoice Small)，提供毫秒级实时反馈。
- 目的不是高精度，而是让用户知道“Agent 听到了什么”。

## 5. 系统架构升级 (Edge vs Brain)

| Layer | Component | Function |
| :--- | :--- | :--- |
| **Edge (Phone)** | VAD & Wake Word | 过滤静音，捕捉意图 |
| **Edge (Phone)** | Context Engine | 采集环境元数据 |
| **Edge (Phone)** | Opus Enc & Crypto | 压缩与加密 (AES-256) |
| **Brain (PC)** | Whisper Large | 全文高精度转录 |
| **Brain (PC)** | Insight Agent | 提取意图与任务 |

## 6. 里程碑

- Phase 1: 稳定 VAD 录音 + Metadata 采集。
- Phase 2: 关键词唤醒 (Porcupine) + 意图标记。
- Phase 3: 实时流式传输 (Real-time Streaming) 对接 Live Agent。
- Phase 4: 端侧 Agent (小模型) 离线应答。
  
- **隐私顾虑**：UI显著提示“所有数据本地加密，仅您可见”。  
- **系统限制**：测试多品牌手机（小米/三星杀后台问题），提供白名单引导。  
- **法律合规**：增加“录音前通知”选项（如弹窗提醒周围人）。
