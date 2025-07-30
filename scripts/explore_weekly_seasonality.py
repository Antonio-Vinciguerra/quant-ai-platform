import os
import pandas as pd

# ===== SETTINGS =====
SYMBOL = "EURUSD"
INPUT_PATH = f"../processed/{SYMBOL}/seasonality_raw.csv"
# ====================

# Load the raw monthly seasonality data
df = pd.read_csv(INPUT_PATH, parse_dates=["Datetime"], index_col="Datetime")

# Create weekday column (0 = Monday, 6 = Sunday)
df["Weekday"] = df.index.weekday
weekday_map = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}
df["Weekday_Name"] = df["Weekday"].map(weekday_map)

# Group by weekday and compute stats
grouped = df.groupby("Weekday_Name").agg({
    "Range_Pips": ["mean", "std"],
    "Body_Pips": "mean",
    "Candle_Type": lambda x: (x == "Bullish").mean()
}).rename(columns={"<lambda_0>": "Bullish_Ratio"})

# Flatten MultiIndex columns
grouped.columns = ["_".join(col).strip("_") for col in grouped.columns.values]

# Reorder by actual weekday order
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
grouped = grouped.loc[day_order]

# Display results
print("\n📊 EURUSD Weekly Seasonality Summary:")
print(grouped.round(2))