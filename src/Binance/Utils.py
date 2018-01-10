#!/usr/bin/python

from time import *

# Set None as no print. 1 as print out debug info.
DEBUG = 1

def get_time_span_seconds(time1, time2):
    pass

def get_time_span_minutes(time1, time2):
    pass

def convert_minute_to_millisec(interval):
    minute = int(interval.strip('m'))
    return minute * 60 * 1000

def get_current_epoch():
    return int(time()) * 1000

def get_float_to_100_percent(f):
    return "{0} %".format((float(f) * 100))

def print_info(info):
    if DEBUG:
        print info
        print "\n"