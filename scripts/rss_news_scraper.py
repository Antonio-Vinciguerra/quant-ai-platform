import json
from datetime import datetime
import feedparser
import os
from bs4 import BeautifulSoup

RSS_FEEDS = {
    "YahooFinance": "https://finance.yahoo.com/rss/topstories",
    "Investing": "https://www.investing.com/rss/news_25.rss",
    "FT": "https://www.ft.com/?format=rss",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "MarketsInsider": "https://markets.businessinsider.com/rss/news",
    "WSJ": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "SeekingAlpha": "https://seekingalpha.com/market_currents.xml"
}

OUTPUT_DIR = "../knowledge_base/raw_scraped"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)

def parse_rss(source_name, url):
    print(f"🔍 Scraping RSS feed: {source_name}")
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            print(f"⚠️ No articles found for {source_name}")
            return []
        articles = []
        for entry in feed.entries[:20]:
            articles.append({
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published", "N/A"),
                "summary": BeautifulSoup(entry.get("summary", ""), "html.parser").text.strip(),
                "source": source_name
            })
        return articles
    except Exception as e:
        print(f"❌ Error scraping {source_name}: {e}")
        return []

def save_articles(source_name, articles):
    filename = f"rss_news_{sanitize_filename(source_name)}_{datetime.utcnow().isoformat()}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        json.dump({
            "source": source_name,
            "timestamp": datetime.utcnow().isoformat(),
            "articles": articles
        }, f, indent=2)
    print(f"✅ Saved {len(articles)} articles from {source_name} to {filepath}")

def main():
    for source, url in RSS_FEEDS.items():
        articles = parse_rss(source, url)
        if articles:
            save_articles(source, articles)

if __name__ == "__main__":
    main()
