import os
import pandas as pd

# ===== SETTINGS =====
SYMBOL = "EURUSD"
FREQ = "D1"
FILE_PATH = f"../processed/{SYMBOL}/{SYMBOL}_{FREQ}.csv"
# ====================

print(f"📥 Loading {SYMBOL} {FREQ} data...")
if not os.path.exists(FILE_PATH):
    print(f"❌ File not found: {FILE_PATH}")
    exit()

# Load data
try:
    df = pd.read_csv(FILE_PATH, parse_dates=["Datetime"])
    df.set_index("Datetime", inplace=True)
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit()

# Add weekday info
df["Day_Name"] = df.index.strftime("%A")
df["Is_Weekend"] = df["Day_Name"].isin(["Saturday", "Sunday"])

# Compute daily range in pips
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000

# 📊 Summary
print("\n📊 EURUSD Daily Range (Pips):")
print(df["Range_Pips"].describe())

# 🗓️ Weekday distribution
print("\n📅 Day of Week Distribution:")
print(df["Day_Name"].value_counts().sort_index())

# 🚫 Weekend candle warning
weekend_count = df["Is_Weekend"].sum()
if weekend_count > 0:
    print(f"\n⚠️ Found {weekend_count} weekend candles — review those rows!")
else:
    print("✅ No weekend candles found. Data looks clean!")