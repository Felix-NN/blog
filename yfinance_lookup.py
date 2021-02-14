#%%
from numpy.core.fromnumeric import std
import yfinance as yf
import random
import pandas as pd
import numpy as np
from googlesearch import search
import csv
import time
import json

# %%
class stock:

    def ticker(self, comp):
        for res in search(comp + 'ticker symbol', tld='com', lang='en', domains=['finance.yahoo.com'], num=1, stop=1):
            res = res.split('/')
            return self.download_history(res[4])

    def download_history(self, symbol):
        data = yf.download(tickers = symbol, period = '1y')
        # If company is not publicly traded write error message
        data = data['Close']
        return self.spikes(data)

    def spikes(self, data):
        stocks = []
        variance = []
        spike_dates = {}
        for dates, price in data.items():
            date = dates.strftime('%Y-%m-%d')
            stocks.append(price)
            if len(stocks) > 7:
                variance.append(std(stocks[-8:-1]))
            else:
                variance.append(std(stocks))
            
            if len(stocks) <= 2:
                spike_dates[date] = 0
                continue
            else:
                pre_var = price - stocks[-2]
            if abs(pre_var) > (variance[-2] * 3):
                spike_dates[date] = 1
            else:
                spike_dates[date] = 0
        spike_dates = pd.DataFrame.from_dict(spike_dates, orient='index', columns=['Spikes'])
        data = data.to_frame().join(spike_dates)
        return self.add_sites(data, company)
        
    def add_sites(self, data, company):
        spike_dates = data.loc[data['Spikes'] == 1]
        web_dates = {}
        for date, value in spike_dates.iterrows():
            date = date.strftime('%Y-%m-%d')
            company_search = company + ' stock ' + date
            rand = random.randrange(100, 200)
            rand = float(rand)
            rand = rand/100
            websites = []
            for res in search(company_search, tld='com', lang='en', num=10, pause=rand, stop=10, tpe='nws'):
                websites.append(res)
            web_dates[date] = websites
        web_dates = pd.Series(web_dates, name='Websites')
        data = data.join(web_dates)
        return data
    
    def routine(self, company):
        data = self.ticker(company)
        data = data.to_json(orient='index', date_format='iso', date_unit='s')
        return data
            
        
    
# %%

# %%
