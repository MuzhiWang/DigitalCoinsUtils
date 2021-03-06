#!/usr/bin/python

import requests
import json
from Utils import *

BASE_URL = "https://api.binance.com/"
PING = "api/v1/ping"
TIME = "api/v1/time"
KLINES = "api/v1/klines"
ALL_PRICES = "api/v1/ticker/allPrices"
DEPTH = "api/v1/depth"
TICKER_24HOURS = "api/v1/ticker/24hr"


def ping():
    url = BASE_URL + PING
    print_info("Calling " + url)
    response = requests.get(url)
    print_info(response)

def get_server_time():
    url = BASE_URL + TIME
    print_info("Calling " + url)
    response = requests.get(url)
    print_info(response)
    print_info(response.content)
    serverTIme = json.loads(response.content)
    return serverTIme["serverTime"]

def get_depth(symbol, limit = None):
    url = "{0}{1}?symbol={2}".format(BASE_URL, DEPTH, symbol)
    if limit is not None:
        url += "&limit={0}".format(limit)
    response = requests.get(url)
    print_info(url)
    content = response.content
    _depth = json.loads(content)
    print_info(_depth)
    return Depth(_depth)

def get_klines(symbol, interval, start_epoch_time = None, end_epoch_time = None):
    if start_epoch_time is None or end_epoch_time is None:
        url = "{0}{1}?symbol={2}&interval={3}".format(BASE_URL, KLINES, symbol, interval)
    else:
        url = "{0}{1}?symbol={2}&interval={3}&startTime={4}&endTime={5}".format(BASE_URL, KLINES, symbol, interval, start_epoch_time, end_epoch_time)
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
    url = BASE_URL + ALL_PRICES
    print_info("Calling " + url)
    response = requests.get(url)
    print_info(response)
    content = response.content
    print_info(content)
    return json.loads(content)

def get_ticker_24hours(symbol=None):
    url = "{0}{1}".format(BASE_URL, TICKER_24HOURS)
    if symbol is not None:
        url = "{0}?&symbol={1}".format(url, symbol)
    print_info("Call url: " + url)
    response = requests.get(url)
    print_info(response)
    content = response.content
    tickers = []

    if symbol is None:
        data = json.loads(content)
        for d in data:
            tickers.append(Ticker(d))
    else:
        data = json.loads(content)
        tickers.append(Ticker(data))

    return tickers




'''
[
    [
        1499040000000,      // Open time
        "0.01634790",       // Open
        "0.80000000",       // High
        "0.01575800",       // Low
        "0.01577100",       // Close
        "148976.11427815",  // Volume
        1499644799999,      // Close time
        "2434.19055334",    // Quote asset volume
        308,                // Number of trades
        "1756.87402397",    // Taker buy base asset volume
        "28.46694368",      // Taker buy quote asset volume
        "17928899.62484339" // Can be ignored
    ]
]
'''
class Line(object):
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

'''
{
  "lastUpdateId": 1027024,
  "bids": [
    [
      "4.00000000",     // PRICE
      "431.00000000",   // QTY
      []                // Can be ignored
    ]
  ],
  "asks": [
    [
      "4.00000200",
      "12.00000000",
      []
    ]
  ]
}
'''
class Depth(object):
    def __init__(self, data):
        # print data["bids"]
        bids = []
        asks = []
        for b in list(data["bids"]):
            bids.append(Depth_Attr(b))
        for a in list(data["asks"]):
            asks.append(Depth_Attr(a))
        self._bids = bids
        self._asks = asks

    @property
    def bids(self):
        return self._bids

    @property
    def asks(self):
        return self._asks

class Depth_Attr(object):
    def __init__(self, data):
        self._price = float(data[0])
        self._qty = float(data[1])

    @property
    def price(self):
        return self._price

    @property
    def qty(self):
        return self._qty

'''
{
    "symbol": "ZRXBTC",
    "priceChange": "0.00001709",
    "priceChangePercent": "11.934",
    "weightedAvgPrice": "0.00015502",
    "prevClosePrice": "0.00014321",
    "lastPrice": "0.00016030",
    "lastQty": "609.00000000",
    "bidPrice": "0.00015958",
    "bidQty": "88.00000000",
    "askPrice": "0.00016030",
    "askQty": "1266.00000000",
    "openPrice": "0.00014321",
    "highPrice": "0.00016440",
    "lowPrice": "0.00014142",
    "volume": "4419186.00000000",
    "quoteVolume": "685.06295847",
    "openTime": 1516335777202,
    "closeTime": 1516422177202,
    "firstId": 1026927,
    "lastId": 1042796,
    "count": 15870
}
'''
class Ticker(object):
    def __init__(self, data):
        self._symbol = data["symbol"]
        self._quote_volume = int(float(data["quoteVolume"]))

    @property
    def symbol(self):
        return self._symbol

    @property
    def quote_volume(self):
        return self._quote_volume


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

# t = get_depth("ETHBTC", 5)
# for i in t.bids:
#     print i.price
#     print i.qty

# t = get_ticker_24hours("ZRXBTC")
# print len(t)
# print t[0].quote_volume
