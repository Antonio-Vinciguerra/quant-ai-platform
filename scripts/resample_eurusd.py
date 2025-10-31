import pandas as pd

# ===== SETTINGS =====
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_file = os.path.join(project_root, 'processed', 'EURUSD_M1_ALL_FILTERED.csv')  # your master M1 file
# ====================

print("⏳ Loading master file (this may take a bit)...")
df = pd.read_csv(input_file, names=["Datetime", "Open", "High", "Low", "Close", "Volume"], header=0, parse_dates=["Datetime"])

# Set Datetime as the index for resampling
df.set_index('Datetime', inplace=True)

# Ensure data is sorted by time
df.sort_index(inplace=True)

# Resample to H1
print("⏳ Resampling to H1...")
H1 = df.resample('1H').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'})
H1.dropna(inplace=True)
H1.to_csv('EURUSD_H1.csv')
print("✅ EURUSD_H1.csv saved")

# Resample to H4
print("⏳ Resampling to H4...")
H4 = df.resample('4H').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'})
H4.dropna(inplace=True)
H4.to_csv('EURUSD_H4.csv')
print("✅ EURUSD_H4.csv saved")

# Resample to D1
print("⏳ Resampling to D1...")
D1 = df.resample('1D').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'})
D1.dropna(inplace=True)
D1.to_csv('EURUSD_D1.csv')
print("✅ EURUSD_D1.csv saved")

# Resample to W1
print("⏳ Resampling to W1...")
W1 = df.resample('1W').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'})
W1.dropna(inplace=True)
W1.to_csv('EURUSD_W1.csv')
print("✅ EURUSD_W1.csv saved")

# Resample to MN1 (monthly)
print("⏳ Resampling to MN1...")
M1 = df.resample('M').agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'})
M1.dropna(inplace=True)
M1.to_csv('EURUSD_MN1.csv')
print("✅ EURUSD_MN1.csv saved")

print("🎉✅ All resampled files are ready!")

def resample_all(symbol="EURUSD"):
    pass  # Placeholder for now
