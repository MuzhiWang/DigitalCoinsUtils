#!/usr/bin/python

from Provider import *
from Utils import *
from time import *

DEFAULT_LINE_INTERVAL = "1m"

def get_compare_info(symbol, interval):
    klines = list(get_klines(symbol, DEFAULT_LINE_INTERVAL))
    current_mill = get_server_time()
    interval_mill = convert_minute_to_millisec(interval)
    latest_line = klines[-1]

    # print current_mill
    # print interval_mill
    # print latest_line.close_time
    # print "current mill above \n"

    for line in reversed(klines):
        # print line.close_time
        if (current_mill - line.close_time) > interval_mill:
            compare_info = Compare_Info()

            # Diff volume
            compare_info.diff_volume = latest_line.volume - line.volume
            volume_increase_rate = float(format((compare_info.diff_volume / line.volume), '.4f'))
            compare_info.volume_increase_rate = volume_increase_rate

            # Diff price
            compare_info.diff_price = latest_line.close - line.close
            price_increase_rate = float(format((compare_info.diff_price / line.close), '.4f'))
            compare_info.price_increase_rate = price_increase_rate

            print_info("latest vol: " + str(latest_line.volume))
            print_info("target vol: " + str(line.volume))
            print_info("latest price: " + str(latest_line.close))
            print_info("target vol: " + str(line.close))
            return compare_info

def get_all_symbols_volume_diff(interval):
    symbols = get_all_symbols()
    for symbol in symbols:
        compare_info = get_compare_info(symbol, interval)
        print_info("{0} volume diff is: {1}".format(symbol, compare_info.diff_volume))

def compare_info_alert(compare_info):
    compare_info = Compare_Info(compare_info)
    # if (compare_info.)


class Compare_Info(object):

    def __init__(self):
        self._diff_volume = None
        self._volume_increase_rate = None
        self._diff_price = None
        self._price_increase_rate = None

    @property
    def diff_volume(self):
        return self._diff_volume

    @diff_volume.setter
    def diff_volume(self, value):
        self._diff_volume = value

    @property
    def volume_increase_rate(self):
        return self._volume_increase_rate

    @volume_increase_rate.setter
    def volume_increase_rate(self, value):
        self._volume_increase_rate = value

    @property
    def diff_price(self):
        return self._diff_price

    @diff_price.setter
    def diff_price(self, value):
        self._diff_price = value

    @property
    def price_increase_rate(self):
        return self._price_increase_rate

    @price_increase_rate.setter
    def price_increase_rate(self, val):
        self._price_increase_rate = val



t = get_compare_info("EOSBTC", "10m")
print t.diff_volume
print t.volume_increase_rate
print_info(t.price_increase_rate)
print get_float_to_100_percent(t.price_increase_rate)

# print get_time()

# get_all_symbols_volume_diff("15m")
