# LifeOS Field Sensor Implementation Guide (Android)

本指南面向 **Swarm Sensory Node** 开发，聚焦：**高灵敏度 VAD + 意图捕捉 + 实时 Context 融合**。

## 1. 核心变更点 (vs Traditional Recorder)

- **Input**: 不只是 Audio，还需要融合 `SensorManager` 数据。
- **Output**: 构造符合 `LifeOS Context API` 的 JSON Payload。
- **Protocol**: 必须实现新的 `POST /ingest/context` 接口调用逻辑。

## 2. 环境准备

- **High Performance Edge**: Snapdragon 8Gen2+ (推荐) 以支持端侧实时模型。
- **Android SDK**: 34+ (Android 14/15 适配 foreground types)。
- **ML Stack**:
  - `sherpa-onnx` (ASR/KWS)
  - `silero-vad` (VAD)

## 3. 模块设计 (Sensory Pipeline)

### 3.1 Context Fusion Engine (New)

```java
// ContextManager.java
public JSONObject snapshotContext() {
    JSONObject ctx = new JSONObject();
    ctx.put("timestamp", Instant.now().toString());
    
    // 1. Location Inference
    if (wifiSSID.equals("MyHomeWiFi")) ctx.put("location", "Home");
    
    // 2. Activity Recognition
    ctx.put("activity", lastDetectedActivity); // e.g., "IN_VEHICLE"
    
    // 3. Device State
    ctx.put("battery", batteryLevel);
    
    return ctx;
}
```

### 3.2 意图检测 (`IntentEngine`)

- **Hotword**: 检测到 "Hey LifeOS" -> 触发 `HighPriorityMode`.
- **Payload Construction**: 将 Audio 文件上传至 NAS 后，立即发送 `POST /ingest/context` 包含 `{ "intent": "command", "audio_ref": "..." }`.

### 3.3 元数据融合 (`ContextFuser`)

```kotlin
data class SegmentMeta(
    val audioHash: String,
    val timeRange: TimeRange,
    val location: GeoPoint?, // <--- New
    val wifiSSID: String?,   // <--- New (Home/Office detection)
    val motionType: String,  // <--- New (Walking/Driving)
    val intentTag: String?   // <--- New (Idea/Command)
)
```

## 4. 关键实施步骤

### Step 1: 建立传感器总线 (Sensor Bus)
- 使用 `Flow` 或 `RxJava` 持续收集 Accelerometer 和 Location 更新。
- 维护一个 `LastKnownContext` 对象。

### Step 2: 升级 VAD 逻辑
- 仅靠音量不够，使用 NLP 模型辅助。
- 引入 **Generic VAD**，过滤掉风噪和车噪。

### Step 3: 实时流式转录 (Visual Feedback)
- 部署 `sherpa-onnx` 的 `sense-voice-small` 量化模型。
- 将识别出的文字实时透传给 UI 层（悬浮窗或通知栏），**不**作为最终结果存储（因为 PC 端会有更好的），只做用户确认用。

### Step 4: 优先级上传队列
- `WorkManager` (Deferrable) -> 普通 VAD 片段。
- `Retrofit/OkHttp Immediate` -> Intent Command 片段 (忽略省电策略)。

## 5. 功耗控制 (Battery Doctor)

- **Geofence**: 在家 (Wi-Fi) 高频采集，外出低频采集。
- **Motion Gating**: 手机静止平放 > 10min -> 降低 VAD 采样率。

## 6. 测试策略

- **Intent Latency**: 从说出 "Hey Agent" 到 PC 端收到 Webhook < 3s。
- **False Acceptance**: 关键词误触率 < 1次/天。


- Opus 编码：建议 16kHz/mono/16kbps~32kbps
- AES-256：每段独立 IV；密钥存于 Android Keystore
- 元数据：时间戳、时长、是否含语音、设备状态

### 4.3 上传机制（先手动）

- 用户触发上传
- 断点续传 & 幂等命名：`{date}/{segmentId}.opus`
- 失败重试 + 仅 Wi-Fi 上传选项

### 4.4 实时转录（可选）

若采用 SenseVoice/QNN：

- 每 5 秒切块送模型（模拟流式）
- 结果拼接显示
- NPU 初始化失败 → CPU fallback

---

## 5. 测试策略（必须做）

### 5.1 单元测试

- VAD 边界：静音→语音→静音场景
- 分段逻辑：最大段长、最小段长、长静音
- 加密/解密正确性（与工具脚本对比）

### 5.2 仪器测试（设备）

- 前台服务常驻 8h+ 稳定性
- 断网/飞行模式 → 恢复上传
- 系统后台限制（小米/三星）

### 5.3 音质与性能评估

- 采样率一致性（16k/mono）
- 语音段漏检率、误检率
- 电量消耗（统计 8h 使用）

### 5.4 关键回归清单

- 录音权限拒绝/恢复
- 通话/其他 App 占用麦克风
- 低电量模式与省电策略

---

## 6. 上线前检查（MVP）

- 前台通知文案清晰、可一键暂停/恢复
- 本地存储清理策略（7/14 天自动清理）
- 数据导出与删除说明
- 隐私提示：录音提示、用户控制权明确

---

## 7. 参考资源

- sherpa-onnx QNN 文档：<https://k2-fsa.github.io/sherpa/onnx/qnn/index.html>
- sherpa-onnx Android 示例：<https://github.com/k2-fsa/sherpa-onnx/tree/master/android/SherpaOnnxSimulateStreamingAsr>
- 模型下载：<https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models-qnn>

---

## 8. 常见问题排查

**Q: 录音一段时间后停止？**  
A: 检查前台服务类型、通知常驻、厂商后台策略白名单。

**Q: NPU 加载失败？**  
A: 验证 QNN 库与设备匹配，fallback 到 CPU 并记录日志。

**Q: 录音断片/漏录？**  
A: 调整 VAD 阈值、最小段长；确认 AudioRecord buffer。

---

本指南会随着项目迭代更新，重点保证手机端模块可持续、低功耗运行，并为主机侧深度处理提供高质量输入。
