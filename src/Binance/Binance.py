#!/usr/bin/python

from Provider import *
from Utils import *
from Default_Settings import *
import time

def get_compare_info(symbol, interval, current_mill):

    print_info("This is get compare info, the symbol is: {0}".format(symbol))

    if symbol is None:
        pass

    klines = list(get_klines(symbol, DEFAULT_LINE_INTERVAL))
    interval_mill = convert_minute_to_millisec(interval)
    latest_line = klines[-1]

    print_info("interval mill is:" + str(interval_mill))
    print_info("lastest line close price is {0}, volume is {1}".format(latest_line.close, latest_line.volume))

    zero_point = None
    for line in reversed(klines[:-1]):
        # If the interval is set as min 1 min, directly check the value nearest to the latest one.
        if (current_mill - line.close_time) > interval_mill or interval_mill == 6000:
            # Skip if the zero point happened before.
            if line.volume < 0.1 or line.close < 0.000000001:
                if zero_point is not None:
                    continue

            print_info("This is set compare info, the symbol is: {0}".format(symbol))
            compare_info = Compare_Info(symbol)

            try:
                # Diff volume
                compare_info.diff_volume = latest_line.volume - line.volume
                volume_increase_rate = float(format((compare_info.diff_volume / line.volume), '.4f'))
                compare_info.volume_increase_rate = volume_increase_rate

                # Diff price
                compare_info.diff_price = latest_line.close - line.close
                price_increase_rate = float(format((compare_info.diff_price / line.close), '.4f'))
                compare_info.price_increase_rate = price_increase_rate

                compare_info.price = latest_line.close

                print_info("latest vol: " + str(latest_line.volume))
                print_info("target vol: " + str(line.volume))
                print_info("latest price: " + str(latest_line.close))
                print_info("target vol: " + str(line.close))
                return compare_info
            except ZeroDivisionError, e:
                zero_point = 1
                # print_error("Error occurred in symbol: {0}. ".format(symbol) + str(e))


def check_all_symbols(interval):
    symbols = get_all_symbols()
    check_symbols(symbols, interval)

def check_symbols(symbols, interval):
    print_info("----------------------- Start check -----------------------")
    print_info("Start to check all symbols price and volume changes...")
    print_info("Current symbols: {0}".format(symbols))

    current_mill = get_server_time()
    print_info("Current mill is: {0}".format(current_mill))

    count = 0
    for symbol in symbols:
        if count < 0:
            break
        print_info("This is check all symbols, the symbol is: {0}".format(symbol))
        compare_info = get_compare_info(symbol, interval, current_mill)
        if compare_info is None:
            print_error("Empty compared info for symbol: {0}".format(symbol))
            continue

        print_info("{0} volume diff is: {1}".format(symbol, str(compare_info.diff_volume)))
        compare_info_alert(compare_info)
        time.sleep(SCAN_EACH_SYMBOL_DELAY)
        count += 1

    print_info("The check all symbols completed.")

def compare_info_alert(compare_info, client_settings = None):
    print_info("This is compare info alert, the symbol is: {0}".format(compare_info.symbol))
    print_info(compare_info.price_increase_rate)

    if client_settings is None:
        client_settings = Client_Settings()

    if compare_info.price_increase_rate > client_settings.price_increase_rate_threshold:
        if compare_info.volume_increase_rate > client_settings.volume_increase_rate_threshold:
            print_info("The {0} is increasing dramatically around: {1}. ".format(compare_info.symbol, get_current_time()), 1)
            print_info("The price at checking time is: {0}".format(compare_info.price), 1)
            print_info("The price increase rate is: {0}".format(get_float_to_100_percent(compare_info.price_increase_rate)), 1)
            print_info("The volume increase rate is: {0}".format(get_float_to_100_percent(compare_info.volume_increase_rate)), 1)
            print_info("*********************** GOOD LUCK! ************************", 1)


# Compare info class represents the difference we want to check from target Line value.
class Compare_Info(object):

    def __init__(self, symbol):
        self._symbol = symbol
        self._price = None
        self._diff_volume = None
        self._volume_increase_rate = None
        self._diff_price = None
        self._price_increase_rate = None

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, val):
        self._symbol = val

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, val):
        self._price = val

    @property
    def diff_volume(self):
        return self._diff_volume

    @diff_volume.setter
    def diff_volume(self, value):
        self._diff_volume = float(value)

    @property
    def volume_increase_rate(self):
        return self._volume_increase_rate

    @volume_increase_rate.setter
    def volume_increase_rate(self, value):
        self._volume_increase_rate = float(value)

    @property
    def diff_price(self):
        return self._diff_price

    @diff_price.setter
    def diff_price(self, value):
        self._diff_price = float(value)

    @property
    def price_increase_rate(self):
        return self._price_increase_rate

    @price_increase_rate.setter
    def price_increase_rate(self, val):
        self._price_increase_rate = float(val)


# Client settings class override the default settings to check compare results, which will trigger alerts.
class Client_Settings(object):

    def __init__(self):
        self._price_increase_rate_threshold = DEFAULT_PRICE_INCREASE_RATE_THRESHOLD
        self._volume_increase_rate_threshold = DEFAULT_VOLUME_INCREASE_RATE_THRESHOLD

    @property
    def price_increase_rate_threshold(self):
        return self._price_increase_rate_threshold
    @price_increase_rate_threshold.setter
    def price_increase_rate_threshold(self, val):
        self._price_increase_rate_threshold = val

    @property
    def volume_increase_rate_threshold(self):
        return self._volume_increase_rate_threshold
    @volume_increase_rate_threshold.setter
    def volume_increase_rate_threshold(self, val):
        self._volume_increase_rate_threshold = val


# t = get_compare_info("EOSBTC", "10m")
# print t.diff_volume
# print t.volume_increase_rate
# print_info(t.price_increase_rate)
# print get_float_to_100_percent(t.price_increase_rate)

# print get_time()

# tt = get_all_symbols()
# print str(tt)


# check_all_symbols("2m")

# ttt = "abcdef"
# print ttt[-3:]
# print ttt[:-1]
# print ttt[1:]

# t = get_server_time()
# tt = get_compare_info("EVXBTC", "2m", t)

# t = get_current_date(1)
# print t
# write_data(t)
