import pandas as pd

df = pd.read_csv("../processed/EURUSD/EURUSD_W1.csv", parse_dates=["Datetime"])
df["Range_Pips"] = (df["High"] - df["Low"]) * 10000
print(df["Range_Pips"].describe())