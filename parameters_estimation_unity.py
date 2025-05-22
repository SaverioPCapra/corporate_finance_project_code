import pandas as pd
import numpy as np

# Load market data
data = pd.read_excel("corporate_finance/U_stockhist.xlsx", index_col=0, parse_dates=True)

# Compute log returns and estimate volatility
log_returns = np.log(data["Price"]).diff().dropna()
std = log_returns.std()
volatility = std * np.sqrt(12)  # Convert monthly volatility to annualized volatility

ev = 16184.91
risk_free_rate = 0.0399


