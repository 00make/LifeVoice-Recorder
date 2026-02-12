# LifeOS SOP Registry (Tactical Manuals)

此目录存储 **LifeOS Active Strategy Room** 的所有标准作业程序 (Standard Operating Procedures)。

## 1. 目录结构

- `SOP_000_Template.md` - 新建 SOP 的标准模板。
- `SOP_*.md` - 实际运行的战术文件。

## 2. 如何添加新 SOP

1. 复制 Template。
2. 定义 `triggers` (Orchestrator 如何找到它)。
3. 定义 `roles` (需要什么配置的 Agent)。
4. 编写 `Steps` (具体的执行逻辑)。

## 3. SOP 生命周期

1. **Draft**: 手动编写或由 `Distiller Agent` 自动生成的草稿。
2. **Active**: 被放入此文件夹，且通过校验 (`schema_version` 匹配)。
3. **Running**: 被 `Context Watcher` 激活，正在被 `SOP Engine` 执行。
4. **Archived**: 旧版本移入 `/archive`。

## 4. 调试

运行测试脚本验证 SOP 逻辑：
```bash
python ../brain/sop_engine.py --sop ./SOP_001_Morning_Briefing.md
```
