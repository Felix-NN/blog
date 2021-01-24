#%%
import yfinance as yf
import pandas as pd
from googlesearch import search
import csv

# %%
def ticker(comp):
    for res in search(comp + 'ticker symbol', tld='com', lang='en', domains=['finance.yahoo.com'], num=1, stop=1):
        res = res.split('/')
        return res[4]

# %%
def download_history(symbol):
    data = yf.download(tickers = symbol, period = '1y')
    data = data['Close']
    return data

# %%
symbol = ticker('microsoft')
data = download_history(symbol)
data.plot()
# %%
