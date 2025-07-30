import pandas as pd

# Load daily file
df = pd.read_csv("../processed/EURUSD/EURUSD_D1.csv", parse_dates=["Datetime"])
df.set_index("Datetime", inplace=True)

# Compute range in pips
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000

# Show stats
print("📊 EURUSD Daily Range (Pips):")
print(df["Range_Pips"].describe())