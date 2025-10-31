import requests
import json
import os
import pandas as pd
import pytz
from datetime import datetime, timedelta

# === Load credentials ===
config_path = os.path.join(os.path.dirname(__file__), 'providers.json')
with open(config_path, 'r') as f:
    config = json.load(f)

oanda_cfg = config['oanda']
ACCOUNT_ID = oanda_cfg['account_id']
API_KEY = oanda_cfg['api_key']
ENV = oanda_cfg['environment']
SYMBOLS = oanda_cfg['symbols']
GRANULARITIES = oanda_cfg['granularities']

# === API setup ===
domain = "api-fxpractice.oanda.com" if ENV == "practice" else "api-fxtrade.oanda.com"
headers = {"Authorization": f"Bearer {API_KEY}"}

def fetch_candles(symbol, granularity, start_time):
    url = f"https://{domain}/v3/instruments/{symbol}/candles"
    params = {
        "granularity": granularity,
        "price": "M",
        "from": start_time,
        "count": 5000
    }

    all_data = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"❌ Error fetching {symbol} {granularity}: {response.text}")
            break

        data = response.json()
        candles = data.get("candles", [])
        if not candles:
            break

        for candle in candles:
            if candle['complete']:
                dt = candle['time']
                mid = candle['mid']
                row = {
                    "Datetime": dt,
                    "Open": mid['o'],
                    "High": mid['h'],
                    "Low": mid['l'],
                    "Close": mid['c'],
                    "Volume": candle['volume']
                }
                all_data.append(row)

        # move the time window
        last_time = candles[-1]['time']
        params["from"] = last_time

        if len(candles) < 5000:
            break

    df = pd.DataFrame(all_data)
    if not df.empty:
        df["Datetime"] = pd.to_datetime(df["Datetime"]).dt.tz_convert("UTC")
    return df

# === Directory setup ===
project_root = os.path.dirname(os.path.dirname(__file__))
raw_root = os.path.join(project_root, "raw")
os.makedirs(raw_root, exist_ok=True)

# === Main loop ===
for symbol in SYMBOLS:
    for granularity in GRANULARITIES:
        print(f"📥 Fetching {symbol} ({granularity}) from Oanda...")

        raw_dir = os.path.join(raw_root, symbol)
        os.makedirs(raw_dir, exist_ok=True)

        file_path = os.path.join(raw_dir, f"{symbol}_{granularity}_ALL.csv")

        # Load existing file if any
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path)
            last_time = pd.to_datetime(df_existing["Datetime"]).max()

            # fix tz handling
            if last_time.tzinfo is None:
                last_time = last_time.tz_localize("UTC")
            else:
                last_time = last_time.tz_convert("UTC")

            start_time = (last_time + timedelta(minutes=1)).isoformat()
        else:
            # Default to last 30 days
            start_time = (datetime.now(pytz.UTC) - timedelta(days=30)).isoformat()

        df_new = fetch_candles(symbol, granularity, start_time=start_time)

        if not df_new.empty:
            if os.path.exists(file_path):
                df_existing = pd.read_csv(file_path)
                df_all = pd.concat([df_existing, df_new]).drop_duplicates(subset="Datetime")
            else:
                df_all = df_new

            df_all.to_csv(file_path, index=False)
            print(f"✅ Updated {file_path} ({len(df_new)} new rows)")
        else:
            print(f"⚠️ No new data for {symbol}")

print("🎯 All symbols fetched and saved successfully.")
