# 📊 Quant Core Concepts & Tools

This document introduces key statistical concepts and tools used in quantitative trading workflows. Each concept is explained in simple terms, with notes on its relevance to trading performance.

---

## 🧠 Core Concepts

- **IQR (Interquartile Range)**  
  Measures the middle 50% of a dataset (between the 25th and 75th percentiles).  
  ➤ **Why it matters**: Helps identify price or volume outliers that could distort models or signals.

- **Z-Score**  
  Indicates how many standard deviations a data point is from the mean.  
  ➤ **Why it matters**: Useful for detecting anomalies in returns, spreads, or volatility.

- **Distribution Histograms**  
  Visual charts showing the frequency distribution of a variable (e.g., price, range, volume).  
  ➤ **Why it matters**: Helps traders understand normal vs extreme behavior in markets.

- **Outlier Detection**  
  The process of identifying unusual data points.  
  ➤ **Why it matters**: Critical for cleaning noisy market data before signal generation.

- **Volatility Metrics**  
  Includes standard deviation, pip range, and average true range (ATR).  
  ➤ **Why it matters**: Quantifies market movement and risk; foundational for position sizing.

- **Seasonality Analysis**  
  Identifies calendar-based patterns (e.g., monthly returns, day-of-week effects).  
  ➤ **Why it matters**: Reveals repeatable market behaviors for strategy design.

---

## 🧰 Tools & Libraries

| Library        | Purpose                            |
|----------------|------------------------------------|
| `pandas`       | Data manipulation, time series     |
| `numpy`        | Numerical operations, statistics   |
| `matplotlib`   | Basic plotting                     |
| `seaborn`      | Statistical visualizations         |
| `plotly`       | Interactive charts and dashboards  |
| `scipy.stats`  | Statistical tests and distributions|
| `statsmodels`  | Time series modeling, regressions  |