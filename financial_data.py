import yfinance as yf
import pandas as pd
from data.subsidiaries import subsidiaries_dict

tickers = subsidiaries_dict.keys()

print("Fetching data from Yahoo Finance...")

data_list = []

for ticker in tickers:
    print(f'fetching {ticker}')
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        data_list.append({
            'Ticker': ticker,
            'Price': info.get('currentPrice'),
            'P/E Ratio': info.get('trailingPE'),
            'Forward P/E': info.get('forwardPE'),
            'Dividend Yield (%)': info.get('dividendYield', 0) if info.get('dividendYield') else 0,
            'Market Cap (B)': info.get('marketCap', 0) / 1e9
        })
    except Exception as e:
        print(f"Could not fetch data for {ticker}: {e}")

# Create a DataFrame
financials = pd.DataFrame(data_list)

# Sort by Dividend Yield for example
financials_sorted = financials.sort_values('Dividend Yield (%)', ascending=False).reset_index(drop=True)

print(financials_sorted.round(2))

# Optional: Save to CSV
financials_sorted.to_csv('utility_financials.csv', index=False)