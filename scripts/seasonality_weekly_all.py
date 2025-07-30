import pandas as pd
import os
from pipeline import get_filtered_data

# === CONFIG ===
SYMBOL = "EURUSD"
TIMEFRAMES = ["H1", "H4", "D1", "W1", "MN1"]
OUTPUT_DIR = "../output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for freq in TIMEFRAMES:
    print(f"\n📅 Loading {SYMBOL} {freq} data from processed...")
    df = get_filtered_data(SYMBOL, freq)

    # Ensure Datetime is a column
    if "Datetime" not in df.columns:
        if df.index.name == "Datetime" or df.index.name is not None:
            df["Datetime"] = df.index
        else:
            print("❌ 'Datetime' column not found!")
            print("🔍 Available columns:", df.columns.tolist())
            continue

    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df["Day_Name"] = df["Datetime"].dt.day_name()

    # Calculate features
    df["Range_Pips"] = (df["High"] - df["Low"]) * 10000
    df["Body_Pips"] = abs(df["Close"] - df["Open"]) * 10000

    # Group by weekday
    grouped = df.groupby("Day_Name").agg({
        "Range_Pips": ["mean", "std"],
        "Body_Pips": "mean",
        "Close": lambda x: (x > df.loc[x.index, "Open"]).mean()
    })

    # Clean columns
    grouped.columns = ["Range_Pips_mean", "Range_Pips_std", "Body_Pips_mean", "Bullish_Ratio"]
    grouped = grouped.sort_values(by="Range_Pips_mean", ascending=False)

    # Save
    output_file = f"{OUTPUT_DIR}/{SYMBOL}_{freq}_weekday_seasonality.csv"
    grouped.to_csv(output_file)
    print(f"\n📊 {freq} Weekday Seasonality Summary:")
    print(grouped)
    print(f"\n✅ Saved to {output_file}")