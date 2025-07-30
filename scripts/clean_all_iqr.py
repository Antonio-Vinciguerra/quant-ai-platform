import os
import pandas as pd

# ===== SETTINGS =====
SYMBOL = "EURUSD"
TIMEFRAMES = ["H1", "H4", "D1", "W1", "MN1"]
INPUT_FOLDER = f"../processed/{SYMBOL}"
OUTPUT_FOLDER = f"../processed/{SYMBOL}/cleaned_iqr"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# ====================

def clean_with_iqr(df):
    df = df.copy()
    df["Range_Pips"] = (df["High"] - df["Low"]) * 10000
    q1 = df["Range_Pips"].quantile(0.25)
    q3 = df["Range_Pips"].quantile(0.75)
    iqr = q3 - q1
    upper_threshold = q3 + 1.5 * iqr
    clean_df = df[df["Range_Pips"] <= upper_threshold]
    flagged_df = df[df["Range_Pips"] > upper_threshold]
    return clean_df, flagged_df, upper_threshold

for tf in TIMEFRAMES:
    path = os.path.join(INPUT_FOLDER, f"{SYMBOL}_{tf}.csv")
    if not os.path.exists(path):
        print(f"❌ Missing file for {tf}")
        continue

    print(f"\n📥 Loading {SYMBOL} {tf} data from {path}...")
    df = pd.read_csv(path, parse_dates=["Datetime"])
    df.set_index("Datetime", inplace=True)

    clean_df, flagged_df, threshold = clean_with_iqr(df)

    clean_path = os.path.join(OUTPUT_FOLDER, f"{SYMBOL}_{tf}_CLEAN.csv")
    flagged_path = os.path.join(OUTPUT_FOLDER, f"{SYMBOL}_{tf}_FLAGGED.csv")
    clean_df.to_csv(clean_path)
    flagged_df.to_csv(flagged_path)

    print(f"🚨 {tf} → Outlier Threshold: {threshold:.2f} pips")
    print(f"✅ {tf} → Clean: {len(clean_df)} | Flagged: {len(flagged_df)}")