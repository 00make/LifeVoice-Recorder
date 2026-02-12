# LifeOS Context Sensor PRD (Data Definition)

## 1. 产品名称

**LifeOS Context Definition**（Context 数据结构与采集标准）

*注：本 PRD 主要包含传感器数据的**结构定义**与**融合逻辑**，物理采集端实现请参考 `Android端录音模块PRD.md`。*

## 2. 产品目标

核心目标：**消除 Agent 的“幻觉”与“盲区”**。
通过物理世界的传感器数据，给 Agent 提供 Ground Truth (事实基础)。
为战情室提供 **Context Awareness** 的数据底座。

## 3. 核心数据维度 (The Context Dimension)

### 3.1 生理感知 (Bio-Signal) -> State Node

- **Data Source**: Wear OS / Garmin / Oura Ring API.
- **Fields**:
  - `heart_rate`: BPM (int).
  - `hrv_stress`: 0-100 (int).
  - `energy_battery`: Body Battery (0-100).
- **Inference**: High Stress + Low Energy = **Defense Mode** (拦截非紧急通知).

### 3.2 环境感知 (Ambient Sense) -> Context Node

- **Data Source**: Android Sensor API.
- **Fields**:
  - `ambient_light`: Lux.
  - `noise_level`: dB.
  - `connectivity`: Wifi SSID, Bluetooth Devices.
- **Inference**: Car Bluetooth Connected + High Noise = **Driving Mode**.

### 3.3 行为感知 (Activity Recog) -> Context Node

- **Data Source**: Android Activity Recognition API.
- **Fields**:
  - `activity_type`: STILL, WALKING, RUNNING, IN_VEHICLE.
  - `app_usage`: Foreground App Package Name.
- **Inference**: App=TikTok + Activity=STILL = **Doomscrolling Mode** (Requires Intervention).

## 4. 融合逻辑 (Context Fusion)

将上述离散数据流融合为可以在 Neo4j 图谱中查询的 **Input Nodes**。

- **Snapshot Frequency**: 每 5 分钟或 `Event Trigger` 时生成一个 Snapshot。
- **Semantic Tagging**:
  - `30.6N, 104.0E` -> `Semantic: Home`
  - `Wifi: Office_5G` -> `Semantic: Office`

## 5. 接口定义

参考 `高性能PC处理API规范.md` 中的 `/ingest/context` 接口。

## 4. 数据融合策略

- **Context Snapshot**: 每当用户触发 LifeVoice Recorder 录音时，与其时间戳同步生成一份 JSON 快照，作为 Prompt 的 System Message 部分注入。

## 5. 里程碑

- Phase 1: Android 基础传感器 (Loc, Activity).
- Phase 2: Wear OS 手表应用 (HR, Sleep).
- Phase 3: Home Assistant 接入 (家庭 IoT 状态).
