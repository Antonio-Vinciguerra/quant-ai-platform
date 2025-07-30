import os
import pandas as pd

# === CONFIG ===
SYMBOL = "EURUSD"
TIMEFRAME = "W1"  # Choose from M1, H1, H4, D1, W1, MN1
PROCESSED_FOLDER = "../processed"
filepath = os.path.join(PROCESSED_FOLDER, SYMBOL, f"{SYMBOL}_{TIMEFRAME}.csv")

# === LOAD DATA ===
print(f"📥 Loading {SYMBOL} {TIMEFRAME} data from {filepath}...")
df = pd.read_csv(filepath, parse_dates=["Datetime"])
df.set_index("Datetime", inplace=True)

# === CALCULATE RANGE ===
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000

# === DESCRIPTIVE STATS ===
print("\n📊 Descriptive Stats for Range (in Pips):")
print(df["Range_Pips"].describe())

# === IQR OUTLIER DETECTION ===
Q1 = df["Range_Pips"].quantile(0.25)
Q3 = df["Range_Pips"].quantile(0.75)
IQR = Q3 - Q1
threshold = Q3 + 1.5 * IQR

print(f"\n🚨 Outlier Threshold (IQR Method): {threshold:.2f} pips")
outliers = df[df["Range_Pips"] > threshold]
print(f"Found {len(outliers)} outliers out of {len(df)} rows.")

# === OPTIONAL: Show Top 10 Extreme Outliers ===
print("\n🔍 Top 10 Outliers:")
print(outliers.sort_values(by="Range_Pips", ascending=False).head(10))