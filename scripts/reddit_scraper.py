import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import praw

# === Load Environment ===
load_dotenv(dotenv_path="../.env")
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# === Initialize Reddit API ===
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET,
    user_agent=USER_AGENT
)

# === Keywords to search ===
KEYWORDS = [
    "EURUSD", "prop trading", "risk management", "macroeconomics",
    "technical analysis", "trading psychology", "inflation", "interest rates"
]

# === Scraper function ===
def scrape_reddit(keyword):
    try:
        print(f"🔍 Scraping Reddit for: {keyword}")
        posts = []
        for submission in reddit.subreddit("all").search(keyword, sort="new", limit=20):
            posts.append({
                "title": submission.title,
                "score": submission.score,
                "url": submission.url,
                "created_utc": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                "subreddit": str(submission.subreddit),
                "permalink": f"https://www.reddit.com{submission.permalink}"
            })

        output = {
            "keyword": keyword,
            "timestamp": datetime.utcnow().isoformat(),
            "posts": posts
        }

        filename = f"../knowledge_base/raw_scraped/reddit_{keyword.replace(' ', '_')}_{datetime.utcnow().isoformat()}.json"
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        print(f"✅ Saved {len(posts)} posts to {filename}")

    except Exception as e:
        print(f"❌ Error scraping {keyword}: {str(e)}")

# === Run all ===
if __name__ == "__main__":
    for kw in KEYWORDS:
        scrape_reddit(kw)
        time.sleep(3)  # delay to avoid rate limits
