#!/usr/bin/python

from crontab import CronTab
import sys, getopt
from Binance import *

def main(argv):
   interval = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["interval="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <interval=2m>'
         sys.exit()
      elif opt in ("-i", "--interval"):
          interval = arg
   print 'The interval is ', interval

   run_cron_job(interval)

def run_cron_job(interval):
   while 1:
      try:
         check_all_symbols(interval)
         time.sleep(CRON_JOB_TIME)
      except:
         print_error("Error happened in Cron job, retry...")


if __name__ == "__main__":
   main(sys.argv[1:])

