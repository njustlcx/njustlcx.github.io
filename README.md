# 小驴哥AI笔记

一个基于 GitHub Pages 的个人技术博客，主题聚焦大模型相关内容，包括：

- 大模型基础概念
- 大模型应用开发
- RAG
- Agent 与工具调用
- 工具链
- 评测与部署

当前站点采用 Markdown 写作、静态 HTML 发布的方式。日常只需要在 `posts/<分类>/` 下新增或修改 `.md` 文件；推送到 `master` 后，GitHub Actions 会自动生成首页、分类首页和文章页。

## 在线地址

- GitHub Pages: `https://njustlcx.github.io/`

## 项目结构

```text
.
├── css/
│   └── main.css
├── js/
│   └── site.js
├── posts/
│   ├── app-dev/
│   │   ├── index.html
│   │   ├── llm-app-stack.md
│   │   └── llm-app-stack/
│   │       └── index.html
│   ├── rag/
│   │   ├── index.html
│   │   ├── rag-basics.md
│   │   └── rag-basics/
│   │       └── index.html
│   └── toolbox/
│       ├── index.html
│       ├── llm-toolbox.md
│       └── llm-toolbox/
│           └── index.html
├── scripts/
│   └── build.py
├── .github/
│   └── workflows/
│       └── build-blog.yml
├── index.html
└── README.md
```

## 页面说明

- `index.html`
  - 由 Markdown 元数据生成的博客首页
  - 包含分类目录、最新文章、分类文章列表和站点访问量展示
- `css/main.css`
  - 全站样式
  - 包括浅色、绿色、深色主题和文章页样式
- `js/site.js`
  - 主题切换
  - 自定义强调色保存到 `localStorage`
- `posts/<分类>/*.md`
  - 各篇文章的 Markdown 源文件
  - `posts/` 下的一级目录就是文章分类
  - 文件头部 front matter 保存标题、摘要、分类名、分类说明和排序
- `posts/<分类>/index.html`
  - 由 Markdown 自动生成的分类首页
- `posts/<分类>/<文章>/index.html`
  - 由 Markdown 自动生成的静态文章页面
  - 每篇文章包含单篇访问量展示
- `scripts/build.py`
  - Markdown 到静态 HTML 的构建脚本
- `.github/workflows/build-blog.yml`
  - 推送 Markdown 后自动运行构建并提交生成页面

## 本地预览

在项目根目录运行：

```bash
python3 -m http.server 4173
```

然后访问：

```text
http://localhost:4173/
```

## 访问量统计

当前站点使用 Busuanzi 前端统计方案：

- 首页展示站点总访问量和访客数
- 文章页展示单篇阅读量和站点访问量

说明：

- 这是第三方前端统计，不需要后端
- 统计数据不是从仓库本地文件开始累加
- 如果第三方脚本不可用，页面仍可正常访问，只是数字不会显示

## 如何新增或修改文章

文章正文优先编辑 Markdown 文件，例如：

```text
posts/rag/rag-basics.md
```

新增文章时：

1. 选择或新建分类目录，例如 `posts/rag/`
2. 在分类目录下新建 Markdown 文件，例如 `posts/rag/my-new-post.md`
3. 参考现有文章的 front matter 填写 `slug`、`title`、`description`、`category`、`category_description`、`category_order`、`order`、`reading_time`、`summary` 和 `date`
4. 编写 Markdown 正文
5. 提交并推送到 `master`

推送后 GitHub Actions 会自动生成：

```text
index.html
posts/<分类>/index.html
posts/<分类>/<文章>/index.html
```

本地如果想提前预览，也可以手动运行一次：

```bash
python3 scripts/build.py
```

但日常新增文章不需要手动运行脚本。
3. 编写 Markdown 正文
## Front Matter 示例

```yaml
---
slug: rag-basics
title: RAG 的核心概念与落地边界
description: 从工程视角理解 RAG 的切分、召回、重排、生成和评估。
category: RAG
category_description: 文档处理、召回、重排、引用和知识库评估。
category_order: 1
order: 1
reading_time: 7 min
summary: RAG 不是“向量库 + 大模型”的简单拼接，而是一条从数据治理到答案评估的链路。
date: 2026-05-06
---
```

## 如何修改主题

可以通过两种方式调整：

1. 页面右上和首页主题面板中直接切换
2. 修改 `css/main.css` 中的颜色变量，例如：

```css
:root {
  --bg: #f7f9fb;
  --surface: #ffffff;
  --text: #18202b;
  --accent: #2563eb;
}
```

## 部署方式

当前仓库直接作为 GitHub Pages 源仓库使用。推送到 `master` 后，自动构建工作流会提交生成页面；GitHub Pages 随后发布最新静态站点。

常用命令：

```bash
git add -A
git commit -m "update blog"
git push origin master
```

## 后续可扩展方向

- 增加更多大模型专题文章
- 增加文章列表页和标签页
- 替换为可控的自建访问量统计
- 增加 SEO 元信息和社交分享卡片
