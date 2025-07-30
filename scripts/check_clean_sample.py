import pandas as pd

# Load only first 1000 rows to check structure
df = pd.read_csv("EURUSD_M1_ALL_CLEAN.csv", nrows=1000)
print(df.head())
print(df.info())