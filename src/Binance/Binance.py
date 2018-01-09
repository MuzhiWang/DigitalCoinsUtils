#!/usr/bin/python

from Provider import *
from Utils import *
from time import *

DEFAULT_LINE_INTERVAL = "1m"

def get_volume_diff(symbol, interval):
    klines = get_klines(symbol, DEFAULT_LINE_INTERVAL)
    current_mill = get_current_epoch()
    interval_mill = convert_minute_to_millisec(interval)
    latest_line = klines[0]

    # print current_mill
    # print interval_mill
    # print latest_line.close_time
    # print "current mill above \n"


    for line in reversed(klines):
        # print line.close_time
        if (current_mill - line.close_time) > interval_mill:
            return latest_line.volume - line.volume

def get_all_symbols_volume_diff(interval):
    symbols = get_all_symbols()
    for symbol in symbols:
        volume_diff = get_volume_diff(symbol, interval)
        print "{0} volume diff is: {1}".format(symbol, volume_diff)


# t = get_volume_diff("LTCBTC", "15m")
# print t

# print get_time()

get_all_symbols_volume_diff("15m")
