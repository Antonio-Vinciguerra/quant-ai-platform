import os
import pandas as pd

PROCESSED_FOLDER = "../processed/EURUSD"
TIMEFRAMES = ["H1", "H4", "D1", "W1", "MN1"]

STATIC_THRESHOLDS = {
    "H1": 100,
    "H4": 200,
    "D1": 250,
    "W1": 500,
    "MN1": 1000
}

def clean_and_flag_file(tf):
    file_path = os.path.join(PROCESSED_FOLDER, f"EURUSD_{tf}.csv")
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return

    df = pd.read_csv(file_path, parse_dates=["Datetime"])
    df["Range_Pips"] = (df["High"] - df["Low"]) * 10000

    dynamic_threshold = df["Range_Pips"].quantile(0.95)
    static_threshold = STATIC_THRESHOLDS.get(tf, 500)

    df["Flagged"] = (
        (df["Range_Pips"] > dynamic_threshold) |
        (df["Range_Pips"] > static_threshold) |
        (df["Datetime"].dt.dayofweek > 4)
    )

    df_flagged = df[df["Flagged"]]
    df_cleaned = df[~df["Flagged"]]

    df.to_csv(os.path.join(PROCESSED_FOLDER, f"EURUSD_{tf}_FULL.csv"), index=False)
    df_cleaned.to_csv(os.path.join(PROCESSED_FOLDER, f"EURUSD_{tf}_CLEANED.csv"), index=False)
    df_flagged.to_csv(os.path.join(PROCESSED_FOLDER, f"EURUSD_{tf}_FLAGGED.csv"), index=False)

    print(f"✅ {tf} → Clean: {len(df_cleaned)} | Flagged: {len(df_flagged)}")

for tf in TIMEFRAMES:
    clean_and_flag_file(tf)