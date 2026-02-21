# Docs Index (MVP)

目标：本目录是唯一需求真相来源（Single Source of Truth）。
Claude Code 必须按本目录实现，不得“自行发挥”。

文件说明：
- 01_PRD_MVP.md：产品需求与验收标准（已定义 API、去重排序、对话约束、降级策略）
- 02_ARCHITECTURE.md：工程模块边界、目录结构、关键组件职责
- 03_DATA_MODEL.md：Event/Meta/Warning/QuerySpec 等 schema
- 04_API_SPEC.md：/api/search 与 /api/chat 的请求响应、错误码、示例
- 05_PIPELINE_SPEC.md：检索流水线各阶段契约（Provider/Fetcher/Extractor/Dedupe/Ranker）
- 06_CHAT_LANGGRAPH.md：LangGraph 图、节点职责、工具约束（证据引用）
- 07_SOURCES.yaml：固定站点入口清单（你维护的“可抓站点”）
- 08_CATEGORY_MAP.json：类型枚举与关键词映射（分类与抽取）
- 09_FETCH_POLICY.md：requests vs Playwright 的策略与触发条件
- 10_PROMPTS.md：LLM 提示词（仅用于路由/抽取兜底），禁止幻觉
- 11_TEST_PLAN.md：可执行验收用例（与 PRD 对齐）
- 12_RUNBOOK.md：本地运行、环境变量、常见故障排查
- 13_BACKLOG.md：后续迭代清单（非 MVP）
- 14_ADR.md：关键技术决策记录（防止未来自己打自己脸）
