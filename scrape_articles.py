import requests
import os
import re
from datetime import datetime, timezone

SANITY_URL = "https://h5lwhzp1.api.sanity.io/v1/data/query/production"
QUERY = '*[_type == "article" && listed == true] | order(date desc) {\
  _id,\
  title,\
  subtitle,\
  "slug": slug.current,\
  date,\
  category\
}'
OUTPUT_FILE = "articles.md"
BASE_URL = "https://brazilianfinance.com"


def fetch_articles():
    r = requests.get(SANITY_URL, params={"query": QUERY})
    r.raise_for_status()
    return r.json()["result"]


def load_existing_slugs(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath) as f:
        content = f.read()
    return set(re.findall(rf"{re.escape(BASE_URL)}/articles/([\w-]+)", content))


def build_md(articles):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# Brazilian Finance — Articles",
        "",
        f"*Last updated: {now} | Total: {len(articles)} articles*",
        "",
    ]
    for art in articles:
        dt = datetime.fromisoformat(art["date"].replace("Z", "+00:00"))
        date_key = dt.strftime("%Y-%m-%d")
        title = art["title"]
        subtitle = (art.get("subtitle") or "").strip()
        slug = art["slug"]
        category = art.get("category", "")
        url = f"{BASE_URL}/articles/{slug}"

        lines.append(f"## {date_key}")
        lines.append("")
        lines.append(f"- **[{title}]({url})**")
        if category or subtitle:
            parts = []
            if category:
                parts.append(category)
            if subtitle:
                parts.append(subtitle)
            lines.append(f"  — {' — '.join(parts)}")
        lines.append("")

    return "\n".join(lines)


def main():
    articles = fetch_articles()
    existing = load_existing_slugs(OUTPUT_FILE)
    new_articles = [a for a in articles if a["slug"] not in existing]

    if new_articles or not os.path.exists(OUTPUT_FILE):
        content = build_md(articles)
        with open(OUTPUT_FILE, "w") as f:
            f.write(content)
        new_slugs = [a["slug"] for a in new_articles]
        print(
            f"Updated {OUTPUT_FILE} — {len(articles)} total, "
            f"{len(new_articles)} new: {new_slugs}"
        )
    else:
        print(
            f"No new articles. {OUTPUT_FILE} already has {len(articles)} entries."
        )


if __name__ == "__main__":
    main()
