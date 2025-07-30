import os
import pandas as pd

# ===== SETTINGS =====
SYMBOL = "EURUSD"
INPUT_FILE = f"../processed/{SYMBOL}/seasonality_summary.csv"
# ====================

# Load and flatten MultiIndex columns
df = pd.read_csv(INPUT_FILE, index_col=0)

# Flatten columns if they are in MultiIndex format
if isinstance(df.columns, pd.MultiIndex):
    df.columns = ['_'.join(col).strip() for col in df.columns.values]

# Debug print
print("🔍 Column names:", df.columns.tolist())

# Sort by average monthly range
sorted_df = df.sort_values(by="Range_Pips_mean", ascending=False)

# Print summary
print("\n📊 EURUSD Seasonality Summary (Sorted by Volatility):\n")
print(sorted_df.round(2))