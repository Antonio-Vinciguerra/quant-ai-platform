
import os
import pandas as pd

# ===== CONFIGURATION =====
SYMBOL = "EURUSD"
TIMEFRAME = "W1"
THRESHOLD_FACTOR = 1.5
# =========================

input_path = f"../processed/{SYMBOL}/{SYMBOL}_{TIMEFRAME}.csv"
print(f"📥 Loading {SYMBOL} {TIMEFRAME} data from {input_path}...")

if not os.path.exists(input_path):
    print("❌ File not found.")
    exit()

df = pd.read_csv(input_path, parse_dates=["Datetime"])
df.set_index("Datetime", inplace=True)

# Calculate range in pips
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000

# IQR Method for Outlier Detection
q1 = df["Range_Pips"].quantile(0.25)
q3 = df["Range_Pips"].quantile(0.75)
iqr = q3 - q1
threshold = q3 + THRESHOLD_FACTOR * iqr
print(f"🚨 Outlier Threshold (IQR Method): {threshold:.2f} pips")

# Filter
clean_df = df[df["Range_Pips"] <= threshold]
flagged_df = df[df["Range_Pips"] > threshold]

# Save
folder = os.path.dirname(input_path)
clean_df.to_csv(os.path.join(folder, f"{SYMBOL}_{TIMEFRAME}_CLEAN.csv"))
flagged_df.to_csv(os.path.join(folder, f"{SYMBOL}_{TIMEFRAME}_FLAGGED.csv"))

print(f"✅ {TIMEFRAME} → Clean: {len(clean_df)} | Flagged: {len(flagged_df)}")
