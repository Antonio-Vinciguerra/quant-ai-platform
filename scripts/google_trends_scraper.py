# google_trends_scraper.py

import os
import json
import time
import random
import requests
from datetime import datetime
from pytrends.request import TrendReq
import pandas as pd
from bs4 import BeautifulSoup

# === Config ===
KEYWORDS = [
    "EURUSD", "prop trading", "risk management", "macroeconomics",
    "technical analysis", "trading psychology", "inflation", "interest rates"
]
RAW_OUTPUT_DIR = "../knowledge_base/raw_scraped"
os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)

# === Step 1: Get proxies from sslproxies.org ===
def fetch_proxies():
    try:
        tables = pd.read_html("https://www.sslproxies.org/")
        df = tables[0]
        https_proxies = df[df["Https"] == "yes"]
        proxy_list = [f"http://{row['IP Address']}:{row['Port']}" for _, row in https_proxies.iterrows()]
        return proxy_list
    except Exception as e:
        print(f"❌ Failed to fetch proxy list: {e}")
        return []
# === Step 2: Scrape Google Trends using rotating proxies ===
def scrape_google_trends(keyword, proxies):
    for proxy in proxies:
        try:
            print(f"🔍 Scraping Google Trends for: {keyword} using proxy: {proxy}")
            pytrends = TrendReq(proxies={"https": proxy}, timeout=(5, 5))
            pytrends.build_payload([keyword], timeframe="now 7-d", geo="")
            data = pytrends.interest_over_time()

            if data.empty:
                print(f"⚠️ No data found for {keyword}")
                continue

            results = data.reset_index().to_dict(orient="records")
            filename = f"google_trends_{keyword.replace(' ', '_')}_{datetime.now().isoformat()}.json"
            out_path = os.path.join(RAW_OUTPUT_DIR, filename)

            with open(out_path, "w") as f:
                json.dump(results, f, indent=2)

            print(f"✅ Saved {len(results)} rows to {out_path}")
            return  # Stop after first successful scrape

        except Exception as e:
            print(f"❌ Proxy failed for {keyword}: {e}")
            time.sleep(2)  # Wait before next proxy

# === Main ===
if __name__ == "__main__":
    proxies = fetch_proxies()
    if not proxies:
        print("❌ No proxies available. Exiting.")
        exit(1)

    for kw in KEYWORDS:
        scrape_google_trends(kw, proxies)
        time.sleep(3)  # Brief pause between keywords
