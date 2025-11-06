import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv(dotenv_path=os.path.expanduser('~/quant-ai-platform/.env'))

FMP_API_KEY = os.getenv("FMP_API_KEY")

if not FMP_API_KEY:
    raise EnvironmentError("Missing FMP_API_KEY in .env file")

symbol = "EURUSD"
url = f"https://financialmodelingprep.com/api/v3/fx/{symbol}?apikey={FMP_API_KEY}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if not data or not isinstance(data, list):
        raise ValueError("Empty or invalid response from FMP.")

    quote = data[0]
    price = quote.get('bid') or quote.get('ask') or quote.get('price')
    change = quote.get('changes') or 0
    percent_change = quote.get('changesPercentage') or 0

    print(f"EUR/USD: {price}")
    print(f"Change: {change} ({percent_change}%)")

    if percent_change > 0:
        print("📈 Trend: Bullish")
    elif percent_change < 0:
        print("📉 Trend: Bearish")
    else:
        print("➖ Trend: Sideways / Unchanged")

except requests.RequestException as e:
    print("❌ Request failed:", e)
except (ValueError, KeyError, IndexError) as e:
    print("❌ Failed to parse response:", e)
