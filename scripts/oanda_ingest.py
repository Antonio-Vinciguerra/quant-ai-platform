import requests
import json
import os
import pandas as pd
from datetime import datetime, timedelta

# === 1. Load credentials from providers.json ===
config_path = os.path.join(os.path.dirname(__file__), 'providers.json')
with open(config_path, 'r') as f:
    config = json.load(f)

oanda_cfg = config['oanda']
ACCOUNT_ID = oanda_cfg['account_id']
API_KEY = oanda_cfg['api_key']
ENV = oanda_cfg['environment']
SYMBOL = oanda_cfg['symbol']
GRANULARITY = oanda_cfg['granularity']

# === 2. Set Oanda endpoint ===
domain = "api-fxpractice.oanda.com" if ENV == "practice" else "api-fxtrade.oanda.com"
url = f"https://{domain}/v3/instruments/{SYMBOL}/candles"
headers = {"Authorization": f"Bearer {API_KEY}"}

# === 3. Set raw folder path ===
project_root = os.path.dirname(os.path.dirname(__file__))  # go up from /scripts
raw_dir = os.path.join(project_root, 'raw', 'EURUSD')
os.makedirs(raw_dir, exist_ok=True)
raw_file = os.path.join(raw_dir, 'EURUSD_M1_ALL.csv')

# === 4. Find last timestamp ===
if os.path.exists(raw_file):
    df_existing = pd.read_csv(raw_file)
    df_existing['Datetime'] = pd.to_datetime(df_existing['Datetime']).dt.tz_localize('UTC')
    last_time = df_existing['Datetime'].max()
else:
    df_existing = pd.DataFrame()
    last_time = datetime.utcnow() - timedelta(days=1)
# === 5. Fetch new data from Oanda ===
from_time = last_time.strftime('%Y-%m-%dT%H:%M:%SZ')
params = {
    "from": from_time,
    "granularity": GRANULARITY,
    "price": "M",
    "count": 5000
}

print(f"⏳ Fetching data from {from_time}...")
response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    print(f"❌ Error: {response.status_code} - {response.text}")
    exit()

data = response.json()
candles = data.get('candles', [])
rows = []
for c in candles:
    if c['complete']:
        rows.append([
            c['time'],
            float(c['mid']['o']),
            float(c['mid']['h']),
            float(c['mid']['l']),
            float(c['mid']['c']),
            int(c['volume'])
        ])

# === 6. Build DataFrame and rename columns ===
new_df = pd.DataFrame(rows, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
new_df['Datetime'] = pd.to_datetime(new_df['Datetime'])

# === 7. Merge with existing data ===
if not df_existing.empty:
    combined = pd.concat([df_existing, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=['Datetime']).sort_values('Datetime')
else:
    combined = new_df

# === 8. Save updated file ===
combined.to_csv(raw_file, index=False)
print(f"✅ Ingested {len(new_df)} new rows. Total rows: {len(combined)}")

# === 9. Call your pipeline to clean and resample ===
try:
    import sys
    sys.path.append(os.path.join(project_root, 'scripts'))
    from pipeline import clean_data, resample_data
    clean_data('EURUSD')
    resample_data('EURUSD')
    print("✅ Cleaned and resampled data updated.")
except Exception as e:
    print(f"⚠️ Pipeline step skipped: {e}")