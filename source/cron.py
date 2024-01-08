from croniter import croniter
from crontab import CronTab

cron_expression = "*/15 * * * * *"

cron = CronTab(user="ec2-user")

for job in cron:
    if job.setall(cron_expression):
        cron.remove(job)

new_job = cron.new(
    command='/bin/bash -c "sleep 3 && docker exec biscon /usr/bin/python3 /bis/source/test.py"'
)
new_job.setall(cron_expression)

cron.write()
