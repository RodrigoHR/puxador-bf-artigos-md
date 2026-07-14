# puxador-bf-artigos-md

Fetches all articles from [Brazilian Finance](https://brazilianfinance.com/articles) via the Sanity CMS public API and generates/updates a markdown file (`articles.md`) with date, title, subtitle, category, and link for each article.

Changes are automatically committed and pushed to GitHub.

## How to use

Double-click `executar.command`, or run manually:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scrape_articles.py
```

The first run creates `articles.md` with all existing articles. Subsequent runs fetch new articles and append them (ordered by date, newest first).

## Output format

```markdown
# Brazilian Finance — Articles

*Last updated: 2026-07-14 | Total: 29 articles*

## 2026-07-13

- **[Article Title](https://brazilianfinance.com/articles/article-slug)**
  — Category — Subtitle

## 2026-07-09
...
```

## How it works

- Uses the publicly readable Sanity.io API (`projectId: h5lwhzp1`)
- Queries all articles with `*[_type == "article" && listed == true] | order(date desc)`
- Tracks already-saved articles by slug to avoid duplicates
- On new articles: updates `articles.md`, commits, and pushes to GitHub automatically
