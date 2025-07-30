import pandas as pd
import matplotlib.pyplot as plt

# Load the daily data
print("⏳ Loading daily data...")
df = pd.read_csv("EURUSD_D1.csv", parse_dates=['Datetime'])
df.set_index('Datetime', inplace=True)

# Print basic info
print("✅ Data loaded!")
print(df.head())
print("\nSummary statistics:")
print(df.describe())

# Plot closing price over time
print("📈 Plotting closing price...")
plt.figure(figsize=(12,6))
plt.plot(df.index, df['Close'], linewidth=0.5)
plt.title('EUR/USD Daily Close')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.tight_layout()
plt.show()