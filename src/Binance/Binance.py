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

    print_info("latest line close time: " + str(latest_line.close_time))
    print_info("second latest line close time: " + str(klines[-2].close_time))
    print_info("interval mill is:" + str(interval_mill))
    print_info("lastest line close price is {0}, volume is {1}".format(latest_line.close, latest_line.volume))

    reversed_klines = list(reversed(klines[:-1]))
    zero_point = None
    for line in reversed_klines:
        # If the interval is set as min 1 min, directly check the value nearest to the latest one.
        if (current_mill - line.close_time) > interval_mill or interval_mill == 60000:
            # Skip if the zero point happened before.
            if line.volume < 0.001 or line.close < 0.000000001:
                if zero_point is not None:
                    continue
            print_info("current line close time:" + str(line.close_time))
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

def check_depth(symbol):

    ave_bids_weight = 0.0
    ave_asks_weight = 0.0
    for i in range(DEFAULT_DEPTH_CHECK_TIMES):
        depth = get_depth(symbol, limit=10)
        bids = depth.bids
        asks = depth.asks
        bids_weight = 0.0
        asks_weight = 0.0
        count = len(bids)

        for b in bids:
            index = bids.index(b)
            bids_weight += ((1 - (float(index) / 20)) * b.qty)
        for a in asks:
            index = asks.index(a)
            asks_weight += ((1 - (float(index) / 20)) * a.qty)

        print_info("The bids weight is: " + str(bids_weight))
        print_info("The asks weight is: " + str(asks_weight))

        # depth_diff = float((bids_weight - asks_weight) / asks_weight)
        # print_info("The depth diff is: " + str(depth_diff))

        ave_bids_weight += bids_weight
        ave_asks_weight += asks_weight

        time.sleep(DEFAULT_DEPTH_CHECK_INTERVAL)

    depth_diff = float((ave_bids_weight - ave_asks_weight) / ave_asks_weight)
    print_info("The depth diff is: " + str(depth_diff))

    depth_comprare_info = Depth_Compare_Info()
    depth_comprare_info.symbol = symbol
    depth_comprare_info.asks_weight = ave_asks_weight / DEFAULT_DEPTH_CHECK_TIMES
    depth_comprare_info.bids_weight = ave_bids_weight / DEFAULT_DEPTH_CHECK_TIMES
    depth_comprare_info.diff_weight = depth_diff
    return depth_comprare_info



def check_all_symbols():
    symbols = get_all_symbols()
    check_symbols(symbols)

def check_symbols(symbols):
    print_info("----------------------- Start check -----------------------")
    print_info("Start to check all symbols price and volume changes...")
    print_info("Current symbols: {0}".format(symbols))

    current_mill = get_server_time()
    interval = "1m"
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
            depth_compare_info = check_depth(compare_info.symbol)
            if depth_compare_info.diff_weight >= DEFAULT_DEPTH_DIFF:
                print_info("The {0} is increasing dramatically around: {1}. ".format(compare_info.symbol, get_current_time()), 1)
                print_info("The price at checking time is: {0}".format(compare_info.price), 1)
                print_info("The price increase rate is: {0}".format(get_float_to_100_percent(compare_info.price_increase_rate)), 1)
                print_info("The volume increase rate is: {0}".format(get_float_to_100_percent(compare_info.volume_increase_rate)), 1)
                print_info("The bids weight is: {0}, asks weight is: {1}, diff weight is: {2}".format(str(depth_compare_info.bids_weight), str(depth_compare_info.asks_weight), get_float_to_100_percent(depth_compare_info.diff_weight)), 1)
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

class Depth_Compare_Info(object):
    def __init__(self):
        self._symbol = None
        self._bids_weight = None
        self._asks_weight = None
        self._diff_weight = None

    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbol(self, val):
        self._symbol = val

    @property
    def bids_weight(self):
        return self._bids_weight
    @bids_weight.setter
    def bids_weight(self, val):
        self._bids_weight = val

    @property
    def asks_weight(self):
        return self._asks_weight
    @asks_weight.setter
    def asks_weight(self, val):
        self._asks_weight = val

    @property
    def diff_weight(self):
        return self._diff_weight
    @diff_weight.setter
    def diff_weight(self, val):
        self._diff_weight = val

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


# check_all_symbols()
# check_symbols(["ZRXBTC"])

# ttt = "abcdef"
# print ttt[-3:]
# print ttt[:-1]
# print ttt[1:]

# t = get_server_time()
# tt = get_compare_info("EVXBTC", "2m", t)

# t = get_current_date(1)
# print t
# write_data(t)

# depth_diff = check_depth("IOTABTC")
# print depth_diff.asks_weight
# print depth_diff.bids_weight
# print depth_diff.diff_weight
# t = (1- (float(0) / 20)) * 10.0
# print(t)
