#!/usr/bin/python

import requests
import json

Base_url = "https://api.binance.com/"
Ping = "api/v1/ping"
Time = "api/v1/time"
Klines = "api/v1/klines"
All_Prices = "api/v1/ticker/allPrices"

def ping():
    url = Base_url + Ping
    print "Calling " + url
    response = requests.get(url)
    print response
    print "\n"

def get_time():
    url = Base_url + Time
    print "Calling " + url
    response = requests.get(url)
    print response
    print response.content
    print "\n"

def get_klines(symbol, interval):
    url = "{0}{1}?symbol={2}&interval={3}".format(Base_url, Klines, symbol, interval)
    print "Calling " + url
    response = requests.get(url)
    print response
    print "\n"
    content = response.content
    _klines = json.loads(content)
    well_lines = []
    for line in _klines:
        well_line = Line(line)
        well_lines.append(well_line)
    return well_lines

def get_all_symbols():
    all_prices = get_all_prices()
    all_symbols = []
    for price in all_prices:
        # print price['symbol']
        all_symbols.append(price['symbol'])
    # print "\n"
    return all_symbols

def get_all_prices():
    url = Base_url + All_Prices
    print "Calling " + url
    response = requests.get(url)
    print response
    content = response.content
    print content
    return json.loads(content)

class Line(object):
# '''
# [
#     [
#         1499040000000,      // Open time
#         "0.01634790",       // Open
#         "0.80000000",       // High
#         "0.01575800",       // Low
#         "0.01577100",       // Close
#         "148976.11427815",  // Volume
#         1499644799999,      // Close time
#         "2434.19055334",    // Quote asset volume
#         308,                // Number of trades
#         "1756.87402397",    // Taker buy base asset volume
#         "28.46694368",      // Taker buy quote asset volume
#         "17928899.62484339" // Can be ignored
#     ]
# ]
# '''
    def __init__(self, data):
        self.open_time = data[0]
        self.open = data[1]
        self.high = data[2]
        self.low = data[3]
        self.close = data[4]
        self.volume = float(data[5])
        self.close_time = data[6]
        self.quote_asset_volume = data[7]
        self.number_of_trades = data[8]
        self.taker_buy_base_asset_volume = data[9]
        self.taker_buy_quote_assert_volume = data[10]
        self.can_be_ignored = data[11]

    def get_volume(self):
        return self.volume

#
# ping()
#
# get_time()
#
# t = get_klines("LTCBTC", "3m")
# print t.__getitem__(0).volume
# get_all_prices()

# get_all_symbols()