import requests
import json
import os
import pandas as pd
import pytz
from datetime import datetime, timedelta

# === 1. Load config ===
config_path = os.path.join(os.path.dirname(__file__), 'providers.json')
with open(config_path, 'r') as f:
    config = json.load(f)

oanda_cfg = config['oanda']
ACCOUNT_ID = oanda_cfg['account_id']
API_KEY = oanda_cfg['api_key']
ENV = oanda_cfg['environment']
SYMBOLS = oanda_cfg['symbols']
GRANULARITIES = oanda_cfg['granularities']

domain = "api-fxpractice.oanda.com" if ENV == "practice" else "api-fxtrade.oanda.com"
headers = {"Authorization": f"Bearer {API_KEY}"}

# === 2. Helper function ===
def fetch_candles(symbol, granularity, start_time):
    params = {
        "granularity": granularity,
        "from": start_time,
        "price": "M",
        "count": 5000
    }
    url = f"https://{domain}/v3/instruments/{symbol}/candles"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ Failed to fetch {symbol} {granularity}: {response.text}")
        return pd.DataFrame()

    candles = response.json().get("candles", [])
    data = []

    for c in candles:
        time = c["time"]
        o = float(c["mid"]["o"])
        h = float(c["mid"]["h"])
        l = float(c["mid"]["l"])
        cl = float(c["mid"]["c"])
        vol = int(c["volume"])
        data.append([time, o, h, l, cl, vol])

    df = pd.DataFrame(data, columns=["Datetime", "Open", "High", "Low", "Close", "Volume"])
    df["Datetime"] = pd.to_datetime(df["Datetime"]).dt.tz_convert("UTC")
    return df

# === 3. Set raw data path ===
project_root = os.path.dirname(os.path.dirname(__file__))
raw_root = os.path.join(project_root, 'raw')
os.makedirs(raw_root, exist_ok=True)

# === 4. Fetch & save data for all symbols ===
for symbol in SYMBOLS:
    for granularity in GRANULARITIES:
        print(f"📥 Fetching {symbol} ({granularity}) from Oanda...")

        raw_dir = os.path.join(raw_root, symbol)
        os.makedirs(raw_dir, exist_ok=True)

        file_path = os.path.join(raw_dir, f"{symbol}_{granularity}_ALL.csv")

        # Determine start time
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path)
            last_time = pd.to_datetime(df_existing["Datetime"]).max().tz_convert("UTC")
            start_time = (last_time + timedelta(minutes=1)).isoformat()
        else:
            start_time = (datetime.now(pytz.UTC) - timedelta(days=30)).isoformat()  # default: 30 days

        # Fetch
        df_new = fetch_candles(symbol, granularity, start_time)
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
