import pandas as pd

df = pd.read_excel("ReportHistory-1511885501.xlsx", header=None)

# Print the first 30 rows so we can inspect them
for idx, row in df.iterrows():
    print(f"{idx}: {row.values}")
    if idx > 30:
        break
