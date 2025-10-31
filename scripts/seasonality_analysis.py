import pandas as pd
import numpy as np
import os

# === CONFIG ===
SYMBOL = "EURUSD"
FREQ = "D1"  # Change to "W1", "H4", etc.
DATA_PATH = f"../processed/{SYMBOL}/{SYMBOL}_{FREQ}.csv"
OUTPUT_FILE = f"../seasonality/{SYMBOL}_{FREQ}_seasonality_summary.csv"

print(f"📥 Loading {SYMBOL} {FREQ} data from {DATA_PATH}...")

# === LOAD DATA ===
df = pd.read_csv(DATA_PATH, parse_dates=["Datetime"])
if "Datetime" not in df.columns:
    print("❌ 'Datetime' column not found!")
    print(f"🔍 Available columns: {df.columns.tolist()}")
    exit()

df["Month_Name"] = df["Datetime"].dt.strftime("%B")
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000
df["Body_Pips"] = (df["Close"] - df["Open"]).abs() * 10000
df["Candle_Type"] = np.where(df["Close"] > df["Open"], "Bullish", "Bearish")

# === AGGREGATE ===
monthly = df.groupby("Month_Name").agg({
    "Range_Pips": ["mean", "std"],
    "Body_Pips": "mean",
    "Candle_Type": lambda x: (x == "Bullish").mean()
})

monthly.columns = ["Range_Pips_mean", "Range_Pips_std", "Body_Pips_mean", "Bullish_Ratio"]
monthly.index.name = "Month_Name"
monthly = monthly.sort_values(by="Range_Pips_mean", ascending=False)

# === EXPORT ===
os.makedirs("../seasonality", exist_ok=True)
monthly.to_csv(OUTPUT_FILE)
print("✅ Seasonality data saved.")


def analyze_seasonality():
    print("📈 Running seasonality analysis (placeholder)...")
