import os
import time
import json
import datetime
import requests
from dotenv import load_dotenv

# === Load your X (Twitter) API Key ===
load_dotenv()
X_API_KEY = os.getenv("X_API_KEY")

# === Output folder path ===
OUTPUT_FOLDER = "../knowledge_base/raw_scraped"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Headers for Twitter API v2 ===
HEADERS = {
    "Authorization": f"Bearer {X_API_KEY}"
}

# === Keywords to track ===
TOPICS = [
    "EURUSD",
    "prop trading",
    "risk management",
    "macroeconomics",
    "technical analysis",
    "trading psychology",
    "inflation",
    "interest rates"
]

# === Twitter search endpoint (recent search) ===
SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

# === Helper: get current UTC timestamp for filenames ===
def get_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

# === Main scraper function ===
def scrape_topic(topic):
    print(f"🔍 Scraping X for topic: {topic}")
    
    params = {
        "query": topic,
        "max_results": 20,
        "tweet.fields": "created_at,text,lang,author_id"
    }

    try:
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            tweets = response.json().get("data", [])
            filename = f"{OUTPUT_FOLDER}/x_{topic.replace(' ', '_')}_{get_timestamp()}.json"
            with open(filename, "w") as f:
                json.dump(tweets, f, indent=2)
            print(f"✅ Saved {len(tweets)} tweets to {filename}")
        else:
            print(f"❌ Failed to fetch tweets for '{topic}': {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception while scraping {topic}: {str(e)}")

# === Start scraping ===
if __name__ == "__main__":
    for topic in TOPICS:
        scrape_topic(topic)
        time.sleep(6)  # 💤 Add delay to avoid hitting rate limits

    print("🎉 All topics scraped successfully.")
