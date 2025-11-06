import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/quant-ai-platform/.env'))

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    print("❌ Alpha Vantage API key not found in .env")
    exit()

symbol = "EURUSD"
url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={API_KEY}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if "Realtime Currency Exchange Rate" in data:
        rate_info = data["Realtime Currency Exchange Rate"]
        price = float(rate_info["5. Exchange Rate"])
        time = rate_info["6. Last Refreshed"]
        print(f"✅ EUR/USD is currently trading at {price:.5f} (Last updated: {time})")
    else:
        print("❌ Could not retrieve exchange rate. Response:")
        print(data)
except Exception as e:
    print(f"❌ Error fetching data: {e}")

