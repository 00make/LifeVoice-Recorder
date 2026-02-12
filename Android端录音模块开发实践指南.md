# 基于 sherpa-onnx QNN APK 开发 Android AI 语音识别应用的的最佳实践指南

您提到的 APK 文件  
**sherpa-onnx-1.12.23-qnn-arm64-v8a-simulated_streaming_asr-zh_en_ko_ja_yue-5-seconds-sense_voice_2024_07_17_int8.apk**  
是一个预编译的演示应用，使用 **SenseVoice 多语言模型**（支持中文、英文、日文、韩文、粤语），在 Qualcomm NPU（QNN/HTP 后端）上实现**模拟流式**实时语音识别。由于 QNN 不支持动态输入形状，该模型固定处理 **5 秒**音频片段（短于 5 秒会填充，长于 5 秒会截断）。

如果您想基于此开发自己的 AI 应用（例如自定义 UI、集成到其他功能、优化体验），建议不要直接反编译预制 APK，而是从官方开源示例项目入手进行二次开发。下面是完整的最佳实践指南。

### 1. 前提条件与硬件要求

- **设备要求**：必须使用 Qualcomm Snapdragon SM8350（Snapdragon 888）或更高型号（如 SM8450、SM8550、SM8650、SM8750、SM8850 等），这些芯片才支持 HTP（Hexagon Tensor Processor）加速。
- **开发环境**：
  - Android Studio（最新版推荐）
  - Android NDK（r25+）
  - CMake 3.22+
  - Qualcomm QNN SDK（需从 Qualcomm 开发者网站注册下载，设置环境变量 `QNN_SDK_ROOT`）
- **模型特点**：
  - SenseVoice 2024-07-17 int8 量化版本，多语言自动检测。
  - 固定 5 秒输入 → 适合短句实时识别，长语音需分段处理。

### 2. 推荐开发路径：从官方示例项目开始

官方提供了完整的 Android 示例源码：  
<https://github.com/k2-fsa/sherpa-onnx/tree/master/android/SherpaOnnxSimulateStreamingAsr>

这是您提到的预制 APK 的源码基础，直接在此基础上修改是最安全、高效的方式。

#### 详细构建步骤

1. **下载 QNN SDK**  
   从 Qualcomm 开发者网站获取并解压，记住 `QNN_SDK_ROOT` 路径。

2. **克隆 sherpa-onnx 仓库**  

   ```bash
   git clone https://github.com/k2-fsa/sherpa-onnx.git
   cd sherpa-onnx
   ```

3. **构建 Android 共享库（包含 QNN 支持）**  
   参考官方文档（<https://k2-fsa.github.io/sherpa/onnx/qnn/index.html）的> “Build shared libraries” 部分，使用 CMake + NDK 编译 arm64-v8a 架构的 `libsherpa-onnx.so` 等库。

4. **复制 QNN 库文件**  
   将 QNN SDK 中的 `lib/hexagon*`、`lib/libQnnHtp.so` 等库复制到项目 jniLibs/arm64-v8a 目录。

5. **下载模型文件**  
   - 前往 <https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models-qnn>  

   - 将模型文件放入 Android 项目 assets 目录或可读存储路径。

6. **修改示例代码使用您的模型**  
   打开 `android/SherpaOnnxSimulateStreamingAsr` 项目，在 Java/Kotlin 代码中：
   - 修改模型路径配置（通常在 `MainActivity` 或相关类中）
   - 设置语言提示（SenseVoice 支持自动检测，通常无需手动指定）
   - 调整音频录制缓冲区大小（建议 5 秒为单位分段处理）

7. **在 Android Studio 中构建并运行**  
   - 打开项目，同步 Gradle
   - 连接支持的 Qualcomm 手机
   - Build → Generate Signed APK 或直接 Run

### 3. 最佳实践与优化建议

#### 性能优化

- **int8 量化**：您选的模型已是 int8，NPU 利用率最高，延迟最低。
- **固定 5 秒限制处理**：
  - 实时场景：录音 → 每 5 秒切一段 → 送模型 → 拼接结果显示（模拟流式）。
  - 长语音：使用 VAD（语音活动检测）检测端点后分段，避免无意义填充。
- **首次运行慢**：在应用启动时预热 NPU（提前加载模型），或提示用户“首次使用稍慢”。

#### UI/UX 最佳实践

- **实时显示**：边录边显示部分结果（分段识别），提升流畅感。
- **语言自动检测**：SenseVoice 自带语言 ID，无需手动切换。
- **错误处理**：
  - NPU 初始化失败 → 降级到 CPU 运行（sherpa-onnx 支持 fallback）
  - 录音权限、设备不支持提示友好错误。
- **省电与后台**：避免长时间连续录音，使用前台服务 + 部分唤醒。

#### 权限与安全

- 必须声明权限：

  ```xml
  <uses-permission android:name="android.permission.RECORD_AUDIO" />
  <uses-permission android:name="android.permission.FOREGROUND_SERVICE" /> <!-- 如需后台 -->
  ```

- 运行时动态请求录音权限。

#### 测试与调试

- 在多款 Qualcomm 手机测试（888、8 Gen1、8 Gen2、8 Gen3 等）。
- 使用 adb logcat 查看 QNN/Hexagon 日志，检查是否真正跑在 NPU 上。
- 对比 CPU 模式性能差异（关闭 QNN 后端测试）。

#### 许可证注意

- sherpa-onnx 代码：Apache-2.0
- SenseVoice 模型：请查看模型来源的许可证（通常允许商用，但需确认）。

### 4. 其他资源

- 官方 QNN 文档：<https://k2-fsa.github.io/sherpa/onnx/qnn/index.html>
- 模型下载：<https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models-qnn>
- 示例源码：<https://github.com/k2-fsa/sherpa-onnx/tree/master/android/SherpaOnnxSimulateStreamingAsr>
- 社区讨论：GitHub Issues（k2-fsa/sherpa-onnx）

按照以上步骤，您可以快速得到一个稳定、高性能的多语言实时语音识别应用。如果在构建过程中遇到具体错误（如 QNN 库链接问题），欢迎提供错误日志，我可以进一步帮助排查。祝开发顺利！
