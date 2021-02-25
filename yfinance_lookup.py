#%%
from os import name
from numpy.core.fromnumeric import std
import yfinance as yf
import random
import pandas as pd
import numpy as np
from googlesearch import search
import csv
import time
import json

#%%
"""
Brakel, J.P.G. van (2014). "Robust peak detection algorithm using z-scores". Stack Overflow. Available at: https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/22640362#22640362 (version: 2020-11-08).

Using this Python implementation https://stackoverflow.com/a/43512887/12230053

"""

def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            signals[i] = 1
            

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

    return signals

# %%
class stock:

    def ticker(self, comp):
        for res in search(comp + 'ticker symbol', tld='com', lang='en', domains=['finance.yahoo.com'], num=1, stop=1):
            res = res.split('/')
            return self.download_history(res[4])

    def download_history(self, company):
        data = yf.download(tickers = company, period = '1y')
        # If company is not publicly traded write error message
        data = data['Close']
        return self.spikes(data, company)

    def spikes(self, data, company):
        """
        stocks = []
        variance = []
        spike_dates = {}
        pos_neg = []
        pre_var_list = []
        pre_dates = []
        for dates, price in data.items():
            date = dates.strftime('%Y-%m-%d')
            pre_dates.append(date)
            stocks.append(price)
            if len(stocks) > 7:
                variance.append(std(stocks[-8:-1]))
            else:
                variance.append(std(stocks))
            
            if len(stocks) <= 3:
                spike_dates[date] = 0
                pre_var_list.append(0)
                pos_neg.append('')
                continue
            else:
                pre_var = price - stocks[-2]
                pre_var_list.append(pre_var)
                if pre_var > 0:
                    pos_neg.append('pos')
                else:
                    pos_neg.append('neg')
            print(pre_dates[-2], 'pv_list: ', pre_var_list[-2], 'var: ', variance[-2] * 2, ' ', pos_neg[-1], pos_neg[-2], pos_neg[-3])
            if abs(pre_var_list[-2]) > (variance[-2] * 2) and pos_neg[-1] == pos_neg[-3] and pos_neg[-1] != pos_neg[-2]:
                spike_dates[pre_dates[-2]] = 1
                spike_dates[date] = 0
            else:
                spike_dates[date] = 0
        for key, value in spike_dates.items():
            if value == 1:
                print(key)
        """
        result = thresholding_algo(data, lag=5, threshold=3.5, influence=.5)
        dates = []
        for index, value in data.iteritems():
            dates.append(index)
        spike_dates = pd.Series(data=result, index=dates, name='Spikes')
        data = data.to_frame().join(spike_dates)
        return self.add_sites(data, company)
        
    def add_sites(self, data, company):
        spike_dates = data.loc[data['Spikes'] == 1.0]
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
        data = data.rename_axis('Date').reset_index()
        data = data.to_json(orient='index', date_format='iso', date_unit='s')
        return data
            
        
    
# %%

# %%
