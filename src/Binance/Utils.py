#!/usr/bin/python

from time import *

def get_time_span_seconds(time1, time2):
    pass

def get_time_span_minutes(time1, time2):
    pass

def convert_minute_to_millisec(interval):
    minute = int(interval.strip('m'))
    return minute * 60 * 1000

def get_current_epoch():
    return int(time()) * 1000