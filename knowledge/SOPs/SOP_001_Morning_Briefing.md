---
id: "SOP_001_Morning_Briefing"
schema_version: "1.0"
name: "Morning Intelligence Briefing"
description: "早间情报简报：融合天气、日程、身体状态，生成今日策略。"

triggers:
  - type: "time"
    cron: "0 7 * * *"  # 每天早上 7 点
  - type: "context"
    condition: "Activity == 'Waking Up' AND Location == 'Home'"

roles:
  - id: "analyst"
    model: "deepseek-v3" # 需要强推理能力
  - id: "writer"
    model: "qwen2.5-14b-instruct-quant" # 本地生成文本

budget:
  max_tokens: 2000
---

# 1. 任务目标

在用户醒来时，提供一份高信噪比的“作战简报”，而不是简单的“早安”。
简报应包含：
1. **生理状态评估**: 基于昨晚睡眠数据，建议今天的运动量。
2. **环境情报**: 天气与通勤路况。
3. **今日战术**: 基于 Calendar 和 Todo，规划 Top 3 重点。

# 2. 执行步骤

## Step 1: Gather Intelligence (Analyst)

- **Assignee**: `analyst`
- **Action Type**: `ToolCall`
- **Tools**: [`get_sleep_data`, `get_calendar`, `get_weather`, `get_traffic`]
- **Instruction**:
  > 调用所有可用工具获取原始数据。
  > 只要 raw JSON，不需要总结。

## Step 2: Strategic Analysis (Analyst)

- **Assignee**: `analyst`
- **Input Context**: `{{step_1.output}}`
- **Instruction**:
  > 分析数据间的关联：
  > - 如果 Sleep Score < 70 且 Calendar 有 5 个会议 -> 警告：高压力风险，建议取消非必要会议。
  > - 如果 Weather = Rain 且 Traffic = Congested -> 建议：提前 30 分钟出发。
  > 输出格式：JSON, 包含 `strategy_level` (Defense/Attack) 和 `key_advice`.

## Step 3: Draft Briefing (Writer)

- **Assignee**: `writer`
- **Input Context**: `{{step_2.output}}`
- **Instruction**:
  > 使用“参谋长”的口吻（冷静、简洁、专业）。
  > 避免废话。直接给结论。
  > *Example*: "Commander, sleep recovery was optimal (85%). Heavy rain expected at 09:00. Recommend Deep Work block before noon."

# 3. 最终交付

- **TTS**: 发送文本到 Android 端进行语音播报。
- **Notification**: 发送卡片到 Watch。
