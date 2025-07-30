import os
import pandas as pd

# ===== SETTINGS =====
base_folder = "eurusd_HistData"  # where all the month folders are
output_file = "EURUSD_M1_ALL.csv"
# ====================

all_data = []

# Loop through each subfolder
for item in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, item)
    if os.path.isdir(folder_path):
        # Look for CSV files in this folder
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                csv_path = os.path.join(folder_path, file)
                print(f"⏳ Reading {csv_path} ...")
                # Read CSV (HistData format: DATE,TIME,OPEN,HIGH,LOW,CLOSE,VOLUME)
                df = pd.read_csv(csv_path, header=None)
                df.columns = ["Date", "Time", "Open", "High", "Low", "Close", "Volume"]
                # Combine Date and Time into a single datetime
                df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y.%m.%d %H:%M')
                df = df[['Datetime','Open','High','Low','Close','Volume']]
                all_data.append(df)

# Combine all months into one big DataFrame
if all_data:
    full_df = pd.concat(all_data)
    full_df.sort_values(by="Datetime", inplace=True)
    full_df.to_csv(output_file, index=False)
    print(f"✅ Combined CSV saved as {output_file}")
else:
    print("⚠️ No CSV files found!")