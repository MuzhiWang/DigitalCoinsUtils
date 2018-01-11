#!/usr/bin/python

from crontab import CronTab


my_cron = CronTab(user='superegg')
job = my_cron.new(command='python /Users/superegg/PycharmProjects/DigitalCoinsUtils/DigitalCoinsUtils/src/Binance/Provider.py', comment="Test Cron job")
job.minute.every(1)
# job.hour.every(1)
my_cron.write()