# 小驴哥AI笔记

一个基于 GitHub Pages 的个人技术博客，主题聚焦大模型相关内容，包括：

- 大模型基础概念
- 大模型应用开发
- RAG
- Agent 与工具调用
- 工具链
- 评测与部署

当前站点采用纯静态实现，适合直接托管在 `njustlcx.github.io` 仓库中，无需额外构建流程。

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
│   ├── llm-app-stack/
│   │   └── index.html
│   ├── llm-toolbox/
│   │   └── index.html
│   └── rag-basics/
│       └── index.html
├── index.html
└── README.md
```

## 页面说明

- `index.html`
  - 博客首页
  - 包含主题导航、主题目录、专题模块和站点访问量展示
- `css/main.css`
  - 全站样式
  - 包括浅色、绿色、深色主题和文章页样式
- `js/site.js`
  - 主题切换
  - 自定义强调色保存到 `localStorage`
- `posts/*/index.html`
  - 各篇文章的静态页面
  - 每篇文章包含单篇访问量展示

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

## 如何新增文章

1. 在 `posts/` 下新建文章目录，例如：

```text
posts/my-new-post/index.html
```

2. 参考现有文章页面结构编写 HTML 内容
3. 在首页 `index.html` 中对应专题区域加入文章入口

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

当前仓库直接作为 GitHub Pages 源仓库使用，推送到 `master` 分支后即可发布。

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

