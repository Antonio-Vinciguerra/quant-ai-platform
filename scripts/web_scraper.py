# web_scraper.py
# Phase 1: Scrape Q&A data from BabyPips and Reddit to populate knowledge_base/raw_scraped

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# ✅ Search URLs
BABYPIPS_FORUM_URL = "https://forums.babypips.com/c/forex-discussion/11"
REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"

# ✅ Output folder for scraped data
RAW_OUTPUT_DIR = "../knowledge_base/raw_scraped"

# ✅ Headers to mimic real browser (avoid bot block)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; QuantMentorBot/1.0; +http://yourdomain.com)"
}

# ✅ Make sure directory exists
os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)

# === BabyPips Scraper ===
def scrape_babypips(keyword="EURUSD"):
    print(f"🔍 Scraping BabyPips Forum API for: {keyword}")
    url = "https://forums.babypips.com/c/forex-discussion/11.json"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()

    results = []
    for topic in data.get("topic_list", {}).get("topics", []):
        title = topic.get("title", "")
        if keyword.lower() in title.lower():
            results.append({
                "title": title,
                "url": f"https://forums.babypips.com/t/{topic['slug']}/{topic['id']}"
            })

    out_path = os.path.join(RAW_OUTPUT_DIR, f"babypips_{keyword}_{datetime.now().isoformat()}.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Saved {len(results)} BabyPips results to {out_path}")

# === Reddit Scraper ===
def scrape_reddit(keyword="EURUSD"):
    print(f"🔍 Scraping Reddit for: {keyword}")
    params = {"q": keyword, "limit": 20, "sort": "relevance"}
    resp = requests.get(REDDIT_SEARCH_URL, params=params, headers=HEADERS)
    data = resp.json()
    posts = []

    for item in data.get("data", {}).get("children", []):
        post_data = item["data"]
        posts.append({
            "title": post_data.get("title"),
            "selftext": post_data.get("selftext"),
            "url": "https://www.reddit.com" + post_data.get("permalink", "")
        })

    out_path = os.path.join(RAW_OUTPUT_DIR, f"reddit_{keyword}_{datetime.now().isoformat()}.json")
    with open(out_path, "w") as f:
        json.dump(posts, f, indent=2)
    print(f"✅ Saved {len(posts)} Reddit results to {out_path}")


if __name__ == "__main__":
    keywords = ["EURUSD", "risk management", "prop trading", "trading psychology"]
    for kw in keywords:
        scrape_babypips(kw)
       # scrape_reddit(kw)

    print("🎉 Scraping complete!")
