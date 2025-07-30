import pandas as pd

# Load weekly data
df = pd.read_csv("../processed/EURUSD/EURUSD_W1.csv", parse_dates=["Datetime"])
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000

# Show top 10 highest weekly ranges
top_outliers = df.sort_values("Range_Pips", ascending=False).head(10)

print("\n🚨 Top 10 Weekly Outliers by Range (Pips):")
print(top_outliers[["Datetime", "Open", "High", "Low", "Close", "Range_Pips"]])