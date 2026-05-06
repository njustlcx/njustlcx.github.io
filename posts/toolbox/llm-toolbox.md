---
slug: llm-toolbox
title: 个人大模型工具箱清单
description: 大模型开发、评测、检索和部署常用工具选择。
category: 工具链
category_description: 开发框架、向量库、调试、观测和部署工具。
category_order: 3
order: 1
reading_time: 6 min
summary: 工具不是越多越好，关键是覆盖开发、检索、评测、观测和部署这些关键环节。
date: 2026-05-06
---

## 开发框架

原型阶段可以直接使用模型 SDK。流程变复杂后，再引入 LangChain、LlamaIndex 或 Vercel AI SDK 这类框架，减少对话状态、工具调用和流式响应的重复代码。

## 知识库与检索

轻量项目可以从 PostgreSQL + pgvector 开始；数据量和检索策略更复杂时，再考虑 Milvus、Qdrant、Elasticsearch 或混合检索架构。

## 评测工具

promptfoo 适合 prompt 回归测试，Ragas 偏向 RAG 质量评估，DeepEval 可组织更系统的模型输出评测。核心是把评测用例纳入日常迭代。

## 本地与部署

Ollama 适合本地试验，vLLM 适合高吞吐推理服务。生产环境还需要日志、监控、限流、密钥管理和成本告警。
