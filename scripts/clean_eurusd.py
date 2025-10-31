import os
import pandas as pd
from datetime import datetime

def clean_data(pair_name):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_file = os.path.join(project_root, 'raw', pair_name, f"{pair_name}_M1_ALL.csv")
    clean_file = os.path.join(project_root, 'processed', f"{pair_name}_M1_ALL_CLEAN.csv")
    filtered_file = os.path.join(project_root, 'processed', f"{pair_name}_M1_ALL_FILTERED.csv")

    print("⏳ Loading raw data...")
    df = pd.read_csv(raw_file, parse_dates=['Datetime'])

    # Check for duplicates
    if df['Datetime'].duplicated().any():
        print("⚠️ Duplicate timestamps found!")
        df = df[~df['Datetime'].duplicated()]
    else:
        print("✅ No duplicate timestamps found.")

    # Reindex to full minute timeline
    start = df['Datetime'].min()
    end = df['Datetime'].max()
    print(f"⏳ Building full timeline from {start} to {end}...")
    full_range = pd.date_range(start=start, end=end, freq='min')  # every minute

    df.set_index('Datetime', inplace=True)
    df_full = df.reindex(full_range)
    df_full.index.name = 'Datetime'

    print(f"🔎 Missing rows (will show as NaNs): {df_full.isnull().any(axis=1).sum()}")
    df_full.to_csv(clean_file, index_label="Datetime")
    print(f"✅ Saved full timeline with NaNs to {clean_file}")

    # Drop missing
    df_filtered = df_full.dropna()
    print(f"✅ Filtered rows count: {len(df_filtered)}")
    df_filtered.to_csv(filtered_file, index_label="Datetime")
    print(f"✅ Saved filtered dataset (no missing) to {filtered_file}")

    print("🎉✅ Data cleaning completed successfully!")

if __name__ == "__main__":
    clean_data("EURUSD")
