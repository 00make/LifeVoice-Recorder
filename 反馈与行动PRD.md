# LifeOS Action Executor PRD (The Effector / 效应器)

## 1. 产品名称

**LifeOS Effector Node**（LifeOS 效应器节点 / 战术执行终端）

## 2. 产品目标

作为战情室的“手”和“脚”。
不仅是“通知”用户，更是“代表”用户执行 SOP 最终产生的 Action。
连接数字世界 (API) 与物理世界 (IoT) 的 Effectors (效应器)。

## 3. 核心功能架构

### 3.1 战术执行路由 (Tactical Action Router)

- **Input**: Intent JSON (e.g., `{"action": "send_email", "body": "..."}`).
- **Routing**: 将指令分发给对应的 Tool Agent。

### 3.2 工具箱 (The Toolkit)

- **Communication Tool**: 发送 Email, Telegram 消息, Discord Webhook。
- **Coding Tool**: 这里的 Agent 可以 commit code 到 GitHub。
- **IoT Tool**: 控制 Home Assistant 设备。

### 3.3 人机验证 (Human Verification)

- 对于 High Risk Action (如转账、删库、群发邮件)，Executor 会生成一个 **One-Time Token Link** 发送到用户手机。
- 用户点击确认后，Action 才会真正执行。

## 4. 安全协议

- **Sandbox Execution**: 所有 Python 代码执行必须在隔离容器中。
- **Rate Limit**: 限制单位时间内的 API 调用次数。

## 5. 里程碑

- Phase 1: 基础通知与简单的 HTTP GET/POST Webhook。
- Phase 2: 集成 Gmail/Telegram Bot API。
- Phase 3: 完整的 E2B 沙箱代码执行环境。
