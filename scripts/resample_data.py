import os
import pandas as pd

# === Settings ===
RAW_ROOT = "../raw"
PROCESSED_ROOT = "../processed"
SYMBOLS = ["EUR_USD", "GBP_USD", "USD_JPY", "USD_CHF", "AUD_USD", "USD_CAD", "NZD_USD"]
TIMEFRAMES = {
    "M5": "5min",
    "M15": "15min",
    "M30": "30min",
    "H1": "1H",
    "H4": "4H",
    "D1": "1D",
    "W1": "1W",
    "MN1": "1M"
}

def resample_symbol(symbol):
    raw_file = os.path.join(RAW_ROOT, symbol, f"{symbol}_M1_ALL.csv")
    if not os.path.exists(raw_file):
        print(f"❌ No M1 file for {symbol}")
        return

    df = pd.read_csv(raw_file)
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df.set_index("Datetime", inplace=True)

    for tf_code, rule in TIMEFRAMES.items():
        df_resampled = df.resample(rule).agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        }).dropna()

        tf_dir = os.path.join(PROCESSED_ROOT, symbol)
        os.makedirs(tf_dir, exist_ok=True)
        out_path = os.path.join(tf_dir, f"{symbol}_{tf_code}.parquet")
        df_resampled.to_parquet(out_path)
        print(f"✅ Resampled {symbol} to {tf_code} → {out_path}")

# === Run for all symbols ===
for symbol in SYMBOLS:
    resample_symbol(symbol)

print("🎯 All resampling done.")
