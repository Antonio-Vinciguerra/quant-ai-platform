import pandas as pd
import numpy as np

# ===== SETTINGS =====
raw_file = "EURUSD_M1_ALL.csv"  # original dataset
clean_file = "EURUSD_M1_ALL_CLEAN.csv"
filtered_file = "EURUSD_M1_ALL_FILTERED.csv"
# ====================

print("⏳ Loading raw data...")
df = pd.read_csv(raw_file, parse_dates=['Datetime'])
df.sort_values(by='Datetime', inplace=True)
df.set_index('Datetime', inplace=True)

# Report duplicates
duplicates = df.index.duplicated().sum()
if duplicates > 0:
    print(f"⚠️ Found {duplicates} duplicate rows.")
    df = df[~df.index.duplicated(keep='first')]
else:
    print("✅ No duplicate timestamps found.")

# Create a full timeline from first to last timestamp
start = df.index.min()
end = df.index.max()
print(f"⏳ Building full timeline from {start} to {end}...")
full_range = pd.date_range(start=start, end=end, freq='T')  # every minute

# Reindex to full timeline (introduces NaN where data missing)
df_full = df.reindex(full_range)

# Count missing rows
missing_count = df_full.isna().any(axis=1).sum()
print(f"🔎 Missing rows (will show as NaNs): {missing_count}")

# Save the CLEAN file (with NaNs for missing)
df_full.to_csv(clean_file)
print(f"✅ Saved full timeline with NaNs to {clean_file}")

# Create FILTERED dataset (drop rows with any NaNs)
df_filtered = df_full.dropna()
print(f"✅ Filtered rows count: {len(df_filtered)}")
df_filtered.to_csv(filtered_file)
print(f"✅ Saved filtered dataset (no missing) to {filtered_file}")

print("🎉✅ Data cleaning completed successfully!")