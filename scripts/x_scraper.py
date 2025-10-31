# x_scraper.py
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "QuantMentorSentimentBot"
}

QUERY = "EURUSD OR trading psychology OR risk management OR prop trading"
ENDPOINT = "https://api.twitter.com/2/tweets/search/recent"
PARAMS = {
    "query": QUERY,
    "max_results": 20,
    "tweet.fields": "created_at,text,author_id,lang",
}

def fetch_x_posts():
    response = requests.get(ENDPOINT, headers=HEADERS, params=PARAMS)
    if response.status_code != 200:
        print("❌ Error:", response.status_code, response.text)
        return []

    data = response.json()
    timestamp = datetime.utcnow().isoformat()
    save_path = f"../knowledge_base/raw_scraped/x_sentiment_{timestamp}.json"

    with open(save_path, "w") as f:
        import json
        json.dump(data, f, indent=2)

    print(f"✅ Saved {len(data.get('data', []))} tweets to {save_path}")

if __name__ == "__main__":
    fetch_x_posts()
