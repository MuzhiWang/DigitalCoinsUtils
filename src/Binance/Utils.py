#!/usr/bin/python

from Default_Settings import *
import datetime
from time import *

def get_time_span_seconds(time1, time2):
    pass

def get_time_span_minutes(time1, time2):
    pass

def get_current_time(gmt_time = None):
    time_format = "%Y-%m-%d  %H:%M:%S"
    if gmt_time:
        return strftime(time_format, gmt_time())
    return strftime(time_format)

def get_current_date(gmt_time = None):
    date_format = "%Y-%m-%d"
    if gmt_time:
        return strftime(date_format, gmt_time())
    return strftime(date_format)


def convert_minute_to_millisec(interval):
    minute = int(interval.strip('m'))
    return minute * 60 * 1000

def get_current_epoch():
    return int(time()) * 1000

def get_float_to_100_percent(f):
    return "{0} %".format((float(f) * 100))

def write_data(data):
    with open('./Data/dateInfo.txt', 'a') as outFile:
        outFile.write('\n' + str(datetime.datetime.utcnow()) + '  ' + str(data))

def print_info(info, always_display = None):
    if DEBUG or always_display:
        print info
        print "\n"

def print_error(error):
    print_info(error, 1)