#%%
from numpy.core.fromnumeric import std
import yfinance as yf
import pandas as pd
import numpy as np
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
    # If company is not publicly traded write error message
    data = data['Close']
    return data

# %%
def spikes(data):
    stocks = []
    variance = []
    spike_dates = []
    for dates, price in data.items():
        stocks.append(price)
        if len(stocks) > 7:
            variance.append(std(stocks[-8:-1]))
        else:
            variance.append(std(stocks))
        
        if len(stocks) == 1:
            continue
        elif len(stocks) == 2:
            pre_var = price - stocks[0]
        else:
            pre_var = price - stocks[-2]
        if abs(pre_var) > (variance[-2] * 3):
            date = dates.strftime('%y-%m-%d')
            spike_dates.append(date)
    i = 0
    for item in spike_dates:
        print(i, item)
        i += 1
    i = 0
    #while i < len(stocks):
    #    print(data.index[i], stocks[i], variance[i])
    #    i += 1
# %%
#def add_sites(data):
    
# %%
company = 'google'
symbol = ticker(company)
data = download_history(symbol)
spikes(data)
#data.plot()
# %%

# %%
