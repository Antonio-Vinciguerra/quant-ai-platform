import pandas as pd
import openpyxl

INPUT_FILE = "ReportHistory-1511885501.xlsx"
OUTPUT_FILE = "parsed_trade_history.csv"

def find_trade_table_start(df):
    for idx, row in df.iterrows():
        if "Symbol" in row.values and "Volume" in row.values:
            return idx
    return None

try:
    df_raw = pd.read_excel(INPUT_FILE, header=None)
    start_idx = find_trade_table_start(df_raw)

    if start_idx is None:
        print("❌ Could not find the start of the trade table.")
    else:
        df_trades = pd.read_excel(INPUT_FILE, skiprows=start_idx)
        df_trades_cleaned = df_trades.dropna(how="all")

        df_trades_cleaned.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Trade table found at row {start_idx}")
        print(f"✅ Saved cleaned trade data to: {OUTPUT_FILE}")
        print(df_trades_cleaned.head())

except Exception as e:
    print(f"❌ Error processing file: {e}")
