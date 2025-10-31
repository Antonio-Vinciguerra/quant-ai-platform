import os
import json
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

# === Keywords to scrape ===
KEYWORDS = [
    "EURUSD",
    "prop trading",
    "risk management",
    "macroeconomics",
    "technical analysis",
    "trading psychology",
    "inflation",
    "interest rates"
]

# === Output directory ===
OUTPUT_DIR = "../knowledge_base/raw_scraped"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Setup Selenium headless Chrome ===
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f"--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except WebDriverException as e:
        print(f"❌ Error starting Chrome driver: {e}")
        return None

# === Scrape a single keyword ===
def scrape_google_trends(keyword):
    url = f"https://trends.google.com/trends/explore?q={keyword}&geo=US"

    driver = create_driver()
    if not driver:
        return

    try:
        print(f"🔍 Scraping Google Trends for: {keyword}")
        driver.get(url)
        time.sleep(5 + random.uniform(0.5, 2))  # Let page load fully

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Collect basic metadata (page title, raw text)
        data = {
            "keyword": keyword,
            "timestamp": datetime.utcnow().isoformat(),
            "page_title": driver.title,
            "page_text": soup.get_text()
        }

        # Save to file
        filename = f"google_trends_{keyword.replace(' ', '_')}_{datetime.utcnow().isoformat()}.json"
        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Saved data to {output_path}")
    
    except TimeoutException:
        print(f"❌ Timeout for keyword: {keyword}")
    except Exception as e:
        print(f"❌ Error scraping {keyword}: {str(e)}")
    finally:
        driver.quit()

# === Main run ===
if __name__ == "__main__":
    for kw in KEYWORDS:
        scrape_google_trends(kw)
        time.sleep(10 + random.uniform(2, 5))  # Sleep to avoid detection
