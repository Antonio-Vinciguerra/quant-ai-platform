import os
import pandas as pd
from pipeline import get_filtered_data

# ===== SETTINGS =====
OUTPUT_FOLDER = "../processed/EURUSD"
# ====================

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load clean daily data safely
print("📥 Loading daily data...")
df = get_filtered_data("EURUSD", "1D")

# Optional: remove extreme outliers (optional, adjust as needed)
df = df[df['Close'] < 10]

# Group by month
monthly = df.resample("ME").agg({
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last"
})

# Calculate range in pips and body size
monthly["Monthly_Range_Pips"] = (monthly["High"] - monthly["Low"]) * 10000
monthly["Body_Size_Pips"] = (monthly["Close"] - monthly["Open"]).abs() * 10000
monthly["Candle_Type"] = ["Bullish" if c > o else "Bearish" for o, c in zip(monthly["Open"], monthly["Close"])]
monthly = monthly[monthly["Monthly_Range_Pips"] < 2000]
# Save result
out_path = os.path.join(OUTPUT_FOLDER, "monthly_volatility.csv")
monthly.to_csv(out_path)
print(f"✅ Saved monthly volatility to {out_path}")
# Add Year, Month_Name, and Quarter for grouping and analysis
monthly["Year"] = monthly.index.year
monthly["Month_Name"] = monthly.index.strftime("%B")
monthly["Quarter"] = monthly.index.quarter

# Reorder columns
monthly = monthly[[
    "Open", "High", "Low", "Close",
    "Monthly_Range_Pips", "Body_Size_Pips", "Candle_Type",
    "Year", "Month_Name", "Quarter"
]]

# Save again to file
monthly.to_csv(out_path)
print("📊 Monthly volatility file updated with Year, Month and Quarter metadata.")