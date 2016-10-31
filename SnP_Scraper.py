import pandas as pd
import requests
import urllib
import json
import pytz
from bs4 import BeautifulSoup
from datetime import datetime
from pandas.io.data import DataReader
import matplotlib.pyplot as plt

# list of S&P 500 companies for ticker reference
SITE = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# set start and end dates for historical data
START = datetime(2015, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime(2016, 1, 1, 0, 0, 0, 0, pytz.utc)

# scrape wiki page for ticker and sector list
r = urllib.urlopen(SITE).read()
soup = BeautifulSoup(r)

print soup.prettify()[1000:5000]

# using soup.find to isolate table in html file
table = soup.find('table', {'class': 'wikitable sortable'})

# <tr> defines a row, <td> defines a cell in a html table
# dictionary of sectors (keys) with tickers (values)
sector_tickers = dict()

for row in table.findAll('tr'):
    col = row.findAll('td')
    if len(col) > 0:
        sector = str(col[3].string.strip()).lower().replace(' ', '_')
        ticker = str(col[0].string.strip())
        if sector not in sector_tickers:
            sector_tickers[sector] = list()
        sector_tickers[sector].append(ticker)

print sector_tickers

# download open, high, low, close (ohlc) historical data for S&P 500 stocks
# pandas DataReader imports web information into a dataframe
# link to yahoo finance already built into DataReader via 'yahoo' argument
# dictionary iteritems iterates over key, value tuples

sector_ohlc = {}
for sector, ticker in sector_tickers.iteritems():
    print 'downloading data for %s sector' % sector
    data = DataReader(ticker, 'yahoo', START, END)
    for item in ['Open', 'High', 'Low']:
        data[item] = data[item] * data['Adj Close']/data['Close']
    data.rename(items={'Open': 'open', 'High': 'high', 'Low': 'low',
                'Adj Close': 'close', 'Volume': 'volume'}, inplace=True)
    data.drop(['Close'], inplace=True)
    sector_ohlc[sector] = data
print 'finished downloading data'

sector_ohlc['information_technology']
aapl_series = sector_ohlc['information_technology']['close']['AAPL']
aapl_series.plot()
plt.show()

