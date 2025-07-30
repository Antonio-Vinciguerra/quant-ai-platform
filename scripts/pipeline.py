import os
import pandas as pd
import numpy as np

# ===== SETTINGS =====
RAW_FOLDER = "../raw"
PROCESSED_FOLDER = "../processed"
SOURCE_FOLDER = "../source_files"
# ====================

def merge_histdata(symbol: str, source_folder: str = os.path.join(SOURCE_FOLDER, "eurusd_HistData")):
    """
    Merge all monthly CSVs from HistData into one raw file with progress prints.
    """
    csv_files = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    total_files = len(csv_files)
    if total_files == 0:
        print(f"\u26a0\ufe0f No CSV files found in {source_folder}")
        return None

    print(f"\ud83d\udce6 Found {total_files} CSV files to merge from {source_folder}...")
    all_data = []

    for idx, path in enumerate(csv_files, start=1):
        print(f"\u23f3 ({idx}/{total_files}) Reading {path}...")
        try:
            df = pd.read_csv(path, header=None)
            df.columns = ["Date", "Time", "Open", "High", "Low", "Close", "Volume"]
            df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format='%Y.%m.%d %H:%M', errors='coerce')
            df = df[["Datetime", "Open", "High", "Low", "Close", "Volume"]]
            all_data.append(df)
        except Exception as e:
            print(f"\u26a0\ufe0f Skipping {path} due to error: {e}")

    if not all_data:
        print("\u26a0\ufe0f No valid data read.")
        return None

    full_df = pd.concat(all_data)
    full_df.sort_values(by="Datetime", inplace=True)

    out_dir = os.path.join(RAW_FOLDER, symbol)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{symbol}_M1_ALL.csv")

    full_df.to_csv(out_path, index=False)
    print(f"\u2705 Merged data saved to {out_path}")
    return out_path

def clean_data(symbol: str):
    raw_path = os.path.join(RAW_FOLDER, symbol, f"{symbol}_M1_ALL.csv")
    if not os.path.exists(raw_path):
        print(f"\u26a0\ufe0f Raw file not found at {raw_path}")
        return

    print(f"\u23f3 Loading raw data from {raw_path}...")
    df = pd.read_csv(raw_path, parse_dates=["Datetime"])
    df.sort_values(by="Datetime", inplace=True)
    df.set_index("Datetime", inplace=True)

    duplicates = df.index.duplicated().sum()
    if duplicates > 0:
        print(f"\u26a0\ufe0f Found {duplicates} duplicates. Removing...")
        df = df[~df.index.duplicated(keep="first")]
    else:
        print("\u2705 No duplicates found.")

    start, end = df.index.min(), df.index.max()
    full_range = pd.date_range(start=start, end=end, freq="min")
    df_full = df.reindex(full_range)

    missing_count = df_full.isna().any(axis=1).sum()
    print(f"\ud83d\udd0e Missing rows (NaNs): {missing_count}")

    clean_dir = os.path.join(PROCESSED_FOLDER, symbol)
    os.makedirs(clean_dir, exist_ok=True)

    clean_path = os.path.join(clean_dir, f"{symbol}_M1_ALL_CLEAN.csv")
    df_full.to_csv(clean_path)
    print(f"\u2705 CLEAN file saved to {clean_path}")

    filtered_df = df_full.dropna()
    filtered_path = os.path.join(clean_dir, f"{symbol}_M1_ALL_FILTERED.csv")
    filtered_df.to_csv(filtered_path)
    print(f"\u2705 FILTERED file saved to {filtered_path}")

def resample_data(symbol: str):
    filtered_path = os.path.join(PROCESSED_FOLDER, symbol, f"{symbol}_M1_ALL_FILTERED.csv")
    if not os.path.exists(filtered_path):
        print(f"\u26a0\ufe0f Filtered file not found at {filtered_path}")
        return

    df = pd.read_csv(filtered_path, index_col=0, parse_dates=True)
    df.index.name = "Datetime"

    timeframes = {
        "H1": "1H",
        "H4": "4H",
        "D1": "1D",
        "W1": "1W",
        "MN1": "M"
    }

    out_dir = os.path.join(PROCESSED_FOLDER, symbol)
    os.makedirs(out_dir, exist_ok=True)

    for label, freq in timeframes.items():
        print(f"\u23f3 Resampling to {label}...")
        resampled = df.resample(freq).agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })
        resampled.dropna(inplace=True)
        out_path = os.path.join(out_dir, f"{symbol}_{label}.csv")
        resampled.to_csv(out_path)
        print(f"\u2705 Saved {label} data to {out_path}")

def get_filtered_data(symbol: str, freq: str) -> pd.DataFrame:
    FREQ_MAP = {
        "1H": "H1", "H1": "H1",
        "4H": "H4", "H4": "H4",
        "1D": "D1", "D": "D1", "D1": "D1",
        "1W": "W1", "W": "W1", "W1": "W1",
        "1M": "MN1", "MN1": "MN1"
    }

    normalized_freq = FREQ_MAP.get(freq.upper(), freq.upper())
    folder = f"../processed/{symbol}"
    clean_path = os.path.join(folder, f"{symbol}_{normalized_freq}_clean.csv")
    raw_path = os.path.join(folder, f"{symbol}_{normalized_freq}.csv")

    if os.path.exists(clean_path):
        print(f"📥 Loading {symbol} {normalized_freq} data from {clean_path}...")
        df = pd.read_csv(clean_path, parse_dates=["Datetime"])
    elif os.path.exists(raw_path):
        print(f"📥 Loading {symbol} {normalized_freq} data from {raw_path}...")
        df = pd.read_csv(raw_path, parse_dates=["Datetime"])
    else:
        raise FileNotFoundError(f"No file found for {symbol} {normalized_freq} in {folder}")

    df = df.set_index("Datetime").sort_index()
    return df