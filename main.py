import time
from random import randint
import pandas as pd
import plotly.express as px
import data_manager


EPS_LOOKBACK = 5

# Scrape tickers from tradingview.com's high dividend page into a list
ticker_list = data_manager.get_tickers()

# Create lists for each data point to be collected
current_price_list = []
dividend_yield_list = []
annual_dividend_list = []
payout_frequency_list = []
dividend_growth_list = []

# Scrape data from stockanalysis.com and add to the lists
for ticker in ticker_list:
    stock = data_manager.Stock(ticker)
    stock.get_div_info(ticker=stock.ticker)
    current_price_list.append(stock.current_price)
    dividend_yield_list.append(stock.dividend_yield)
    annual_dividend_list.append(stock.annual_dividend)
    payout_frequency_list.append(stock.payout_frequency)
    dividend_growth_list.append(stock.dividend_growth)
    time.sleep(float(f"{randint(0, 1)}" + "." + f"{randint(0, 10)}"))  # 0-2 second sleep to not trigger captcha check

# Create data frame with stock info
data = pd.DataFrame({
    'Ticker': ticker_list,
    'Price': current_price_list,
    'Dividend Yield': dividend_yield_list,
    'Annual Dividend': annual_dividend_list,
    'Payout Frequency': payout_frequency_list,
    'Dividend Growth': dividend_growth_list,
})

# Make a graph using plotly
graph = px.scatter(data, x='Dividend Yield', y='Dividend Growth', hover_name='Ticker', color='Payout Frequency', text='Price')
graph.update_traces(textposition='top right')
graph.update_xaxes(title_text='Dividend Yield')
graph.update_yaxes(title_text='Dividend Growth')
graph.update_layout(title_text='High Dividend Yield Stocks')
graph.show()
