import pandas as pd
from pipeline import get_filtered_data

# === CONFIG ===
SYMBOL = "EURUSD"
FREQ = "D1"
MAX_REASONABLE_RANGE = 1000  # Cap daily range to exclude corrupted candles

print(f"📅 Loading {SYMBOL} {FREQ} data from ../processed/{SYMBOL}/{SYMBOL}_{FREQ}.csv...")
df = get_filtered_data(SYMBOL, FREQ)

# === Reset index to access 'Datetime'
df = df.reset_index()

# === Parse datetime & weekday
df["Datetime"] = pd.to_datetime(df["Datetime"])
df["Day_Name"] = df["Datetime"].dt.day_name()

# === Compute features
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000
df["Body_Pips"] = abs(df["Close"] - df["Open"]) * 10000
df["Bullish"] = df["Close"] > df["Open"]

# === Exclude corrupted data
df = df[df["Range_Pips"] < MAX_REASONABLE_RANGE]

# === Group by weekday
summary = df.groupby("Day_Name").agg({
    "Range_Pips": ["mean", "std"],
    "Body_Pips": "mean",
    "Bullish": "mean"
})

# === Clean columns
summary.columns = ["Range_Pips_mean", "Range_Pips_std", "Body_Pips_mean", "Bullish_Ratio"]
summary = summary.sort_values(by="Range_Pips_mean", ascending=False)

# === Save result
output_file = f"../output/{SYMBOL}_{FREQ}_weekday_seasonality.csv"
summary.to_csv(output_file)

print("\n📊 Weekly Seasonality Summary:")
print(summary)
print(f"\n✅ Saved to {output_file}")