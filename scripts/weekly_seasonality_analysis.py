import os
import pandas as pd
from pipeline import get_filtered_data

# === SETTINGS ===
SYMBOL = "EURUSD"
FREQ = "1D"
OUTPUT_FOLDER = f"../processed/{SYMBOL}"
# ================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("📥 Loading daily data...")
df = get_filtered_data(SYMBOL, FREQ)
df = df[df["Close"] < 10]  # Filter bad data

# Add weekday info
df["Weekday"] = df.index.day_name()

# Calculate pips movement
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000
df["Body_Pips"] = (df["Close"] - df["Open"]).abs() * 10000
df["Candle_Type"] = ["Bullish" if c > o else "Bearish" for o, c in zip(df["Open"], df["Close"])]

# Group by weekday
grouped = df.groupby("Weekday").agg({
    "Range_Pips": ["mean", "std"],
    "Body_Pips": "mean",
    "Candle_Type": lambda x: (x == "Bullish").mean()
})

# Clean column names
grouped.columns = ["Range_Pips_mean", "Range_Pips_std", "Body_Pips_mean", "Bullish_Ratio"]
grouped = grouped.loc[["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]  # order

# Save results
grouped.to_csv(os.path.join(OUTPUT_FOLDER, "weekly_seasonality_summary.csv"))
print("✅ Weekly seasonality saved.")