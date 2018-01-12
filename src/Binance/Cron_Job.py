#!/usr/bin/python

import sys, getopt
from Binance import *
import threading

def main(argv):
   interval = None
   try:
      opts, args = getopt.getopt(argv,"hi:",["interval="])
   except getopt.GetoptError:
      print 'Cron_Job.py -i <interval>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'Cron_Job.py -i <interval=2m>'
         sys.exit()
      elif opt in ("-i", "--interval"):
          interval = arg
   print 'The interval is ', interval

   try:
       parallel_run_job(interval)
   # TODO: This still doesn't work. We need to kill the entire process once we use keyboard.
   except KeyboardInterrupt:
       exit()


def run_cron_job(symbols, interval):
   while 1:
      try:
         check_symbols(symbols, interval)
         time.sleep(CRON_JOB_TIME)
      except KeyboardInterrupt:
         raise
      except:
         print_error("Error happened in Cron job, retry...")

def parallel_run_job(interval):
    # create and start our threads
    threads = list()
    all_symbols = get_all_symbols()
    count = len(all_symbols)
    each_count = int(count / DEFAULT_THREAD)
    for i in range(DEFAULT_THREAD):
        if i == DEFAULT_THREAD - 1:
            symbols = all_symbols[(i * each_count):]
        else:
            start = i * each_count
            end = (i + 1) * each_count
            symbols = all_symbols[start:end]
        print_info("Symbols in thread {0}: {1}, size {2}".format(i, symbols, len(symbols)))
        t = BinanceThread(i)
        t.symbols = symbols
        t.interval = interval
        t.daemon = True
        threads.append(t)
        print_info('Starting Thread {}'.format(i))
        t.start()

    # wait for each to finish (join)
    for i, t in enumerate(threads):
        t.join()
        print_info('Thread {} Stopped'.format(i))

class BinanceThread(threading.Thread):

    #: How long we're going to sleep for
    sleep_length = None

    def __init__(self, sleep_length=None):
        super(BinanceThread, self).__init__()
        self.sleep_length = sleep_length
        self._symbols = None
        self._interval = None

    @property
    def symbols(self):
        return self._symbols
    @symbols.setter
    def symbols(self, val):
        self._symbols = val

    @property
    def interval(self):
        return self._interval
    @interval.setter
    def interval(self, val):
        self._interval = val

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        run_cron_job(self.symbols, self.interval)


if __name__ == "__main__":
   main(sys.argv[1:])

