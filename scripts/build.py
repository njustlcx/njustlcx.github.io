#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "posts"
SITE_TITLE = "小驴哥AI笔记"
SITE_TAGLINE = "LLM Engineering Notes"


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    description: str
    category_slug: str
    category: str
    category_description: str
    category_order: int
    order: int
    reading_time: str
    summary: str
    date: str
    source_path: Path
    body: str

    @property
    def url(self) -> str:
        return f"/posts/{self.category_slug}/{self.slug}/"

    @property
    def category_url(self) -> str:
        return f"/posts/{self.category_slug}/"


def parse_front_matter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} is missing front matter")
    _, front_matter, body = text.split("---\n", 2)
    meta: dict[str, str] = {}
    for line in front_matter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{path} has invalid front matter line: {line}")
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, body.strip()


def parse_int(value: str | None, default: int) -> int:
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def read_posts() -> list[Post]:
    posts: list[Post] = []
    for path in sorted(POSTS_DIR.glob("*/*.md")):
        meta, body = parse_front_matter(path)
        category_slug = path.parent.name
        slug = meta.get("slug", path.stem)
        category = meta.get("category", category_slug)
        title = meta["title"]
        description = meta.get("description", meta.get("summary", title))
        summary = meta.get("summary", description)
        posts.append(
            Post(
                slug=slug,
                title=title,
                description=description,
                category_slug=category_slug,
                category=category,
                category_description=meta.get("category_description", ""),
                category_order=parse_int(meta.get("category_order"), 999),
                order=parse_int(meta.get("order"), 999),
                reading_time=meta.get("reading_time", "5 min"),
                summary=summary,
                date=meta.get("date", ""),
                source_path=path,
                body=body,
            )
        )
    return sorted(posts, key=lambda post: (post.category_order, post.category_slug, post.order, post.title))


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def render_inline(text: str) -> str:
    placeholders: list[str] = []

    def stash(value: str) -> str:
        placeholders.append(value)
        return f"\u0000{len(placeholders) - 1}\u0000"

    def code_repl(match: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(match.group(1))}</code>")

    def link_repl(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        href = escape_attr(match.group(2))
        return stash(f'<a href="{href}">{label}</a>')

    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", code_repl, escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)

    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"\u0000{index}\u0000", value)
    return escaped


def flush_paragraph(lines: list[str], output: list[str], indent: str) -> None:
    if not lines:
        return
    text = " ".join(line.strip() for line in lines)
    output.append(f"{indent}<p>{render_inline(text)}</p>")
    lines.clear()


def markdown_to_html(markdown: str, indent: str = "        ") -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    in_code = False
    code_lines: list[str] = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"{indent}</{list_type}>")
            list_type = None

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            flush_paragraph(paragraph, output, indent)
            close_list()
            if in_code:
                code = html.escape("\n".join(code_lines))
                output.append(f"{indent}<pre><code>{code}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            flush_paragraph(paragraph, output, indent)
            close_list()
            continue

        if line.startswith("### "):
            flush_paragraph(paragraph, output, indent)
            close_list()
            output.append(f"{indent}<h3>{render_inline(line[4:].strip())}</h3>")
            continue

        if line.startswith("## "):
            flush_paragraph(paragraph, output, indent)
            close_list()
            output.append(f"{indent}<h2>{render_inline(line[3:].strip())}</h2>")
            continue

        if line.startswith("> "):
            flush_paragraph(paragraph, output, indent)
            close_list()
            output.append(f"{indent}<blockquote>{render_inline(line[2:].strip())}</blockquote>")
            continue

        if line.startswith("- "):
            flush_paragraph(paragraph, output, indent)
            if list_type != "ul":
                close_list()
                output.append(f"{indent}<ul>")
                list_type = "ul"
            output.append(f"{indent}  <li>{render_inline(line[2:].strip())}</li>")
            continue

        ordered_marker = line.split(".", 1)
        if len(ordered_marker) == 2 and ordered_marker[0].isdigit() and ordered_marker[1].startswith(" "):
            flush_paragraph(paragraph, output, indent)
            if list_type != "ol":
                close_list()
                output.append(f"{indent}<ol>")
                list_type = "ol"
            output.append(f"{indent}  <li>{render_inline(ordered_marker[1].strip())}</li>")
            continue

        close_list()
        paragraph.append(line)

    flush_paragraph(paragraph, output, indent)
    close_list()
    if in_code:
        code = html.escape("\n".join(code_lines))
        output.append(f"{indent}<pre><code>{code}</code></pre>")
    return "\n".join(output)


def group_posts(posts: list[Post]) -> dict[str, list[Post]]:
    groups: dict[str, list[Post]] = {}
    for post in posts:
        groups.setdefault(post.category_slug, []).append(post)
    return groups


def nav_html(categories: list[Post], current: str | None = None) -> str:
    links = ['<a href="/">首页</a>']
    for category in categories:
        active = ' aria-current="page"' if current == category.category_slug else ""
        links.append(f'<a href="{category.category_url}"{active}>{html.escape(category.category)}</a>')
    return "".join(links)


def page_shell(title: str, description: str, body: str, categories: list[Post], current: str | None = None) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f7f9fb">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{escape_attr(description)}">
  <link rel="stylesheet" href="/css/main.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="/" aria-label="{SITE_TITLE} 首页">
      <span class="brand-mark">L</span>
      <span><strong>{SITE_TITLE}</strong><small>{SITE_TAGLINE}</small></span>
    </a>
    <nav class="nav" aria-label="主导航">{nav_html(categories, current)}</nav>
  </header>
{body}
  <script async src="https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
  <script src="/js/site.js"></script>
</body>
</html>
"""


def category_representatives(posts: list[Post]) -> list[Post]:
    representatives: dict[str, Post] = {}
    for post in posts:
        representatives.setdefault(post.category_slug, post)
    return sorted(representatives.values(), key=lambda post: (post.category_order, post.category_slug))


def render_post_card(post: Post) -> str:
    return f"""        <article class="post-card">
          <p class="post-meta">{html.escape(post.category)} · {html.escape(post.reading_time)}</p>
          <h3><a href="{post.url}">{html.escape(post.title)}</a></h3>
          <p>{html.escape(post.summary)}</p>
        </article>"""


def render_home(posts: list[Post]) -> str:
    categories = category_representatives(posts)
    latest = sorted(posts, key=lambda post: (post.date, -post.order), reverse=True)[:6]
    groups = group_posts(posts)
    catalog = "\n".join(
        f"""        <a class="catalog-card" href="{category.category_url}">
          <span>{index:02d}</span>
          <strong>{html.escape(category.category)}</strong>
          <p>{html.escape(category.category_description or f"{len(groups[category.category_slug])} 篇文章")}</p>
        </a>"""
        for index, category in enumerate(categories, 1)
    )
    category_sections = "\n".join(
        f"""    <section class="section" id="{category.category_slug}">
      <div class="section-heading">
        <p class="eyebrow">Category</p>
        <h2>{html.escape(category.category)}</h2>
        <a class="section-link" href="{category.category_url}">查看全部</a>
      </div>
      <div class="post-grid">
{chr(10).join(render_post_card(post) for post in groups[category.category_slug])}
      </div>
    </section>"""
        for category in categories
    )
    latest_cards = "\n".join(render_post_card(post) for post in latest)
    body = f"""
  <main>
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">大模型应用开发 / 工具链 / 概念拆解</p>
        <h1>把大模型能力落到真实产品和工程系统里。</h1>
        <p class="hero-text">这里记录 LLM 应用开发、Agent 设计、RAG、提示词工程、评测、工具调用和模型部署相关的实践笔记。</p>
        <div class="hero-actions">
          <a class="button primary" href="#latest">阅读最新文章</a>
          <a class="button" href="#catalog">浏览分类</a>
        </div>
      </div>
      <aside class="hero-visual" aria-label="大模型工作流示意">
        <div class="pipeline">
          <span>Prompt</span>
          <span>RAG</span>
          <span>Tools</span>
          <span>Eval</span>
        </div>
        <div class="model-card">
          <div class="model-ring"></div>
          <strong>LLM App Stack</strong>
          <p>从原型到上线，关注可观测、可评测、可迭代。</p>
        </div>
      </aside>
    </section>

    <section class="section catalog-section" id="catalog">
      <div class="section-heading">
        <p class="eyebrow">Catalog</p>
        <h2>文章分类</h2>
      </div>
      <div class="catalog-grid">
{catalog}
      </div>
    </section>

    <section class="section" id="latest">
      <div class="section-heading">
        <p class="eyebrow">Latest</p>
        <h2>最新文章</h2>
      </div>
      <div class="post-grid">
{latest_cards}
      </div>
    </section>

    <section class="section" id="theme">
      <div class="section-heading">
        <p class="eyebrow">Theme</p>
        <h2>灵活自定义主题</h2>
      </div>
      <div class="theme-panel" aria-label="主题设置">
        <button class="swatch active" data-theme-choice="light" type="button"><span style="background:#2563eb"></span> 极简蓝</button>
        <button class="swatch" data-theme-choice="mint" type="button"><span style="background:#0f9f6e"></span> 工具绿</button>
        <button class="swatch" data-theme-choice="ink" type="button"><span style="background:#f59e0b"></span> 深色墨</button>
        <label class="custom-color">Accent <input id="accentPicker" type="color" value="#2563eb" aria-label="自定义强调色"></label>
      </div>
    </section>

{category_sections}
  </main>

  <footer class="footer">
    <span>© 2026 {SITE_TITLE}</span>
    <span id="busuanzi_container_site_pv"><span class="visit-stats">站点访问 <strong id="busuanzi_value_site_pv">--</strong></span></span>
    <span id="busuanzi_container_site_uv"><span class="visit-stats">访客 <strong id="busuanzi_value_site_uv">--</strong></span></span>
    <a href="https://github.com/njustlcx/njustlcx.github.io">GitHub</a>
  </footer>
"""
    return page_shell(f"{SITE_TITLE} | 大模型技术博客", "聚焦大模型应用开发、工具链、工程实践和核心概念的个人技术博客。", body, categories)


def render_category(category: Post, posts: list[Post], categories: list[Post]) -> str:
    post_cards = "\n".join(render_post_card(post) for post in posts)
    body = f"""
  <main class="listing-page">
    <section class="article-header">
      <p class="eyebrow">Category</p>
      <h1>{html.escape(category.category)}</h1>
      <p class="hero-text">{html.escape(category.category_description or "这个分类下的全部文章。")}</p>
    </section>
    <section class="section listing-section">
      <div class="post-grid">
{post_cards}
      </div>
    </section>
  </main>
"""
    title = f"{category.category} | {SITE_TITLE}"
    return page_shell(title, category.category_description or title, body, categories, category.category_slug)


def render_article(post: Post, categories: list[Post]) -> str:
    body_html = markdown_to_html(post.body)
    body = f"""
  <main class="article-page">
    <a class="back-link" href="{post.category_url}">返回 {html.escape(post.category)}</a>
    <article>
      <header class="article-header">
        <p class="eyebrow">{html.escape(post.category)} · {html.escape(post.reading_time)}</p>
        <h1>{html.escape(post.title)}</h1>
        <p class="hero-text">{html.escape(post.summary)}</p>
        <div class="article-stats" aria-label="文章访问统计">
          <span id="busuanzi_container_page_pv"><span>本文阅读 <strong id="busuanzi_value_page_pv">--</strong></span></span>
          <span id="busuanzi_container_site_pv"><span>站点访问 <strong id="busuanzi_value_site_pv">--</strong></span></span>
        </div>
      </header>
      <div class="article-content">
{body_html}
      </div>
    </article>
  </main>
"""
    return page_shell(f"{post.title} | {SITE_TITLE}", post.description, body, categories, post.category_slug)


def clean_generated_html() -> None:
    for path in POSTS_DIR.glob("**/index.html"):
        path.unlink()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"built {path.relative_to(ROOT)}")


def main() -> None:
    posts = read_posts()
    if not posts:
        raise SystemExit("No posts found in posts/<category>/*.md")

    clean_generated_html()
    categories = category_representatives(posts)
    groups = group_posts(posts)

    write(ROOT / "index.html", render_home(posts))
    for category in categories:
        category_posts = groups[category.category_slug]
        write(POSTS_DIR / category.category_slug / "index.html", render_category(category, category_posts, categories))
        for post in category_posts:
            write(POSTS_DIR / post.category_slug / post.slug / "index.html", render_article(post, categories))


if __name__ == "__main__":
    main()
