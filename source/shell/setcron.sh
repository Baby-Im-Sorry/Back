#!/bin/bash

echo "*/1 * * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_test.log 2>&1" > /etc/cron.d/cronjob

chmod 0644 /etc/cron.d/cronjob

crontab /etc/cron.d/cronjob