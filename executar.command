#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt -q
fi
.venv/bin/python scrape_articles.py
echo ""
echo "Done. Press Enter to close."
read -r
