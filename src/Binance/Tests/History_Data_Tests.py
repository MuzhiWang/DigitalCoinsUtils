import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from Provider import *
from Utils import *
from Test_Settings import *

def get_test_data(symbol):
    return get_klines(symbol, TEST_INTERVAL, START_EPOCH_TIME, END_EPOCH_TIME)

def simulate_trading(symbol):
    all_data = get_test_data(symbol)

    # Earn type
    EARN_INCREASE = "increase"
    EARN_DECREASE = "decrease"
    EARN_FATAL_DECREASE = "fatal_decrease"
    EARN_FLUCTUATION = "fluctuation"

    buy_price = None
    buy_count = 0
    sold_count = 0
    prev_price = []
    fluctuation_count = 0
    fluctuation_case_count = 0
    decrease_count = 0
    fatal_decrease_count = 0
    # Earn prices contains ("earn_type", buy_price, sell_price, earn_rate, index)
    earn_rate = []

    for data in all_data[1:]:
        index = all_data.index(data)
        current_price = data.close
        current_volume = data.volume
        prev_price = _set_prev_data(all_data, index)
        latest_price_rate_change = _get_price_change_rate(current_price, prev_price[-1].close)

        # Already bought case
        if buy_price is not None:

            # Fatal price decrease case:
            if latest_price_rate_change < FATAL_DECREASE_RATE_SOLD:
                earn_rate.append((EARN_FATAL_DECREASE, buy_price, current_price, _get_price_change_rate(current_price, buy_price), index))
                fatal_decrease_count += 1
                sold_count += 1
                buy_price = None
                fluctuation_count = 0
            # Decrease case:
            elif _get_price_change_rate(current_price, buy_price) < DECREASE_RATE_SOLD:
                earn_rate.append((EARN_DECREASE, buy_price, current_price, _get_price_change_rate(current_price, buy_price), index))
                decrease_count += 1
                sold_count += 1
                buy_price = None
                fluctuation_count = 0
            # Increase case:
            elif latest_price_rate_change >= FLUCTUATION_INCREASE_RATE:
                fluctuation_count = 0
                continue
            # End fluctuation case.
            elif fluctuation_count == FLUCTUATION_TIME_SOLD:
                earn_rate.append((EARN_FLUCTUATION, buy_price, current_price, _get_price_change_rate(current_price, buy_price), index))
                fluctuation_case_count += 1
                sold_count += 1
                buy_price = None
                fluctuation_count = 0
            # Fluctuation case:
            else:
                fluctuation_count += 1
            # else:
            #     print_error("Other case in buy already. Buy price: {0}, current price: {1}, index: {2}. With fluctuation count: {3} ".format(buy_price, current_price, index, fluctuation_count))
        else:
            vol_change_rate = _get_price_change_rate(current_volume, all_data[index - 1].volume)
            if latest_price_rate_change >= EXPECT_INCREASE_RATE and vol_change_rate >= EXPECT_INCREASE_VOL:
                buy_price = current_price
                buy_count += 1
                fluctuation_count = 0

        # print data.close_time

    print "{0} Buy count: {1}, sell count: {2}".format(symbol, buy_count, sold_count)
    return earn_rate


def _set_prev_data(data, index):
    if (index < FLUCTUATION_TIME_SOLD):
        return data[:index]
    else:
        return data[(index - FLUCTUATION_TIME_SOLD):index]

def _init_data(buy_price, fluctuation_count):
    buy_price = None
    fluctuation_count = 0

def _get_price_change_rate(current_price, prev_price):
    try:
        # print float((current_price - prev_price) / prev_price)
        return float((current_price - prev_price) / prev_price)
    except ZeroDivisionError:
        return 1

def test_main():
    symbols = get_all_symbols()
    expectation = 0
    up_count = 0
    down_count = 0

    for symbol in symbols:
        earn_rate = simulate_trading(symbol)
        for earn in earn_rate:
            if earn[3] >= 0:
                up_count += 1
            else:
                down_count += 1
            expectation += earn[3]
            earn_epoch_time = earn[4] * 1000 + START_EPOCH_TIME
            print "Earn type: {0}, earn rate: {1}, with epoch time: {2}".format(earn[0], get_float_to_100_percent(earn[3]), earn_epoch_time)

    print "Entire expectation: {0}, up count: {1}, down count: {2}".format(expectation, up_count, down_count)

def test_symbol(symbol):
    earn_rate = simulate_trading(symbol)
    for earn in earn_rate:
        earn_epoch_time = earn[4] * 1000 + START_EPOCH_TIME
        print "Earn type: {0}, earn rate: {1}, with epoch time: {2}".format(earn[0], get_float_to_100_percent(earn[3]), earn_epoch_time)


# simulate_trading("ETHBTC")


# t = []
# t.append(("t", 0, 1, 2))
# t.append(2)
# print t

# simulate_trading("EOSBTC")


test_main()
# test_symbol("ZRXBTC")