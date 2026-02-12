---
id: "SOP_002_Production_Incident"
schema_version: "1.0"
name: "Server Incident Response"
description: "服务器报警响应流程：自动诊断、日志分析、初步修复。"

triggers:
  - type: "event"
    name: "alert.grafana.webhook"
    params: { severity: "critical" }
  - type: "intent"
    keyword: "Server is down"

roles:
  - id: "sre_bot"
    model: "deepseek-coder-v2" # 强代码能力
    tools: ["ssh_client", "ping", "aws_cli"]

budget:
  max_cost_usd: 0.5
  human_approval: true # 高危操作需确认
---

# 1. 任务目标

当收到 Grafana 报警或用户语音报告宕机时，自动进行 Level 1 诊断，尝试自动恢复或生成详细事故报告。

# 2. 执行步骤

## Step 1: Triage (Initial Diagnosis)

- **Assignee**: `sre_bot`
- **Action Type**: `ToolCall`
- **Instruction**:
  > 1. Ping 目标主机 IP。
  > 2. 如果 Ping 通，SSH 登录执行 `htop` 和 `docker ps`。
  > 3. 如果 Ping 不通，调用 AWS CLI 检查 Instance Status。

## Step 2: Log Analysis

- **Assignee**: `sre_bot`
- **Instruction**:
  > 获取过去 10 分钟的 `error.log` (tail -n 200)。
  > 分析日志中的 Exception Stack Trace。
  > 识别根本原因 (Root Cause)：OOM? Disk Full? Database Connection Timeout?

## Step 3: Mitigation Plan (Critical)

- **Assignee**: `sre_bot`
- **Instruction**:
  > 根据 Root Cause 制定修复计划。
  > - Case OOM: "Restart Docker Container".
  > - Case Disk Full: "Clean /tmp".
  > **注意**: 如果没有明确对应方案，转为“人工介入模式”。

## Step 4: Human Approval

- **Action**: 发送 Action Card 到手机。
  > "Root Cause: Memory Leak in Service X. Plan: Restart Container. [Approve] / [Deny]"
- **Wait**: 等待用户点击。

## Step 5: Execute Fix

- **Trigger**: Only if Step 4 == Approved.
- **Action**: 执行修复命令。

# 3. 最终交付

- **Report**: 生成 Post-Mortem MD 文件存档。
- **Notification**: "Service Recovered. Downtime: 5min."
