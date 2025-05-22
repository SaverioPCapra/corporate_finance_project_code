import pandas as pd
import numpy as np

# Load market data
data = pd.read_excel("corporate_finance/MSFT_stockhist.xlsx", index_col=0, parse_dates=True).sort_index()

# Compute log returns and estimate volatility
log_returns = np.log(data["Price"]).diff().dropna()
std = log_returns.std()
volatility = std * np.sqrt(12)  # Convert monthly volatility to annualized volatility

risk_free_rate = 0.0399

# Compute a reference Microsoft stock price by taking the mean stock price in 2024
msft_stock_price = data["Price"]["2024":].mean()
risk_free_rate = 0.0475
msft_stock_volatility = volatility
msft_credit_spread = 0.0025

print(msft_stock_price)
print(msft_stock_volatility)
