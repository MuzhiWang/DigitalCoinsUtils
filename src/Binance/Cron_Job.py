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

   check_all_symbols(interval)

if __name__ == "__main__":
   main(sys.argv[1:])

