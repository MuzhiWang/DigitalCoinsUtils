#!/usr/bin/python

import requests
import json
from Utils import *

Base_url = "https://api.binance.com/"
Ping = "api/v1/ping"
Time = "api/v1/time"
Klines = "api/v1/klines"
All_Prices = "api/v1/ticker/allPrices"

def ping():
    url = Base_url + Ping
    print_info("Calling " + url)
    response = requests.get(url)
    print_info(response)

def get_server_time():
    url = Base_url + Time
    print_info("Calling " + url)
    response = requests.get(url)
    print_info(response)
    print_info(response.content)
    serverTIme = json.loads(response.content)
    return serverTIme["serverTime"]

def get_klines(symbol, interval):
    url = "{0}{1}?symbol={2}&interval={3}".format(Base_url, Klines, symbol, interval)
    print_info("Calling " + url)
    response = requests.get(url)
    print_info(response)

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
        # Skip the "123456" since it will case float division by zero error for all points since it is testing symbol with all zero data.
        # Also skip "ETH" and "BNB" as compared symbol. We just need "BTC"
        symbol = str(price['symbol'])
        if symbol[-3:] == "BTC":
            all_symbols.append(symbol)
    return all_symbols

def get_all_prices():
    url = Base_url + All_Prices
    print_info("Calling " + url)
    response = requests.get(url)
    print_info(response)
    content = response.content
    print_info(content)
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
        self._open_time = data[0]
        self._open = data[1]
        self._high = data[2]
        self._low = data[3]
        self._close = float(data[4])
        self._volume = float(data[5])
        self._close_time = data[6]
        self._quote_asset_volume = data[7]
        self._number_of_trades = data[8]
        self._taker_buy_base_asset_volume = data[9]
        self._taker_buy_quote_assert_volume = data[10]
        self._can_be_ignored = data[11]

    @property
    def open_time(self):
        return self._open

    @property
    def open(self):
        return self._open

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, value):
        self._high = value

    @property
    def low(self):
        return self._low

    @low.setter
    def low(self, val):
        self._low = val

    @property
    def close(self):
        return self._close

    @close.setter
    def close(self, val):
        self._close = val

    @property
    def close_time(self):
        return self._close_time

    @property
    def quote_asset_volume(self):
        return self._quote_asset_volume

    @property
    def volume(self):
        return self._volume

    @property
    def number_of_trades(self):
        return self._number_of_trades

    @property
    def taker_buy_base_asset_volume(self):
        return self._taker_buy_base_asset_volume


    @property
    def taker_buy_quote_assert_volume(self):
        return self._taker_buy_quote_assert_volume

    @property
    def can_be_ignored(self):
        return self._can_be_ignored

#
# ping()
#
# get_time()
#
# t = get_klines("LTCBTC", "3m")
# print t.__getitem__(0).volume
# get_all_prices()

# data = get_all_symbols()
# print data
# write_data(data)