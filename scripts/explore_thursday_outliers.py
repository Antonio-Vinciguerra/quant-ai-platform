import pandas as pd
from pipeline import get_filtered_data

# === CONFIG ===
SYMBOL = "EURUSD"
FREQ = "D1"

print(f"📅 Loading {SYMBOL} {FREQ} data from ../processed/{SYMBOL}/{SYMBOL}_{FREQ}.csv...")
df = get_filtered_data(SYMBOL, FREQ)

# Ensure Datetime is the index
df.index = pd.to_datetime(df.index)

# Add weekday name
df["Day_Name"] = df.index.day_name()

# Focus on Thursdays
thursdays = df[df["Day_Name"] == "Thursday"].copy()
thursdays["Range_Pips"] = (thursdays["High"] - thursdays["Low"]) * 10000

# Calculate IQR Threshold
q1 = thursdays["Range_Pips"].quantile(0.25)
q3 = thursdays["Range_Pips"].quantile(0.75)
iqr = q3 - q1
threshold = q3 + 1.5 * iqr

outliers = thursdays[thursdays["Range_Pips"] > threshold]

# Show result
print(f"\n🚨 Thursday Range Outlier Threshold: {threshold:.2f} pips")
print(f"Found {len(outliers)} Thursday outliers\n")
print(outliers[["Open", "High", "Low", "Close", "Range_Pips"]].sort_values(by="Range_Pips", ascending=False).head(10))