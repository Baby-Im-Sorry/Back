from croniter import croniter
from crontab import CronTab

cron_expression = '*/30 * * * *'

cron = CronTab(user="ec2-user")

# 이미 해당 작업이 예약되어 있는지 확인
for job in cron:
    if job.setall(cron_expression):
        cron.remove(job)

# 새 작업을 추가합니다
new_job = cron.new(command='/bin/bash -c "sleep 30 && docker exec biscon /usr/bin/python3 /bis/source/test.py"')  # 스크립트 경로를 수정하세요
new_job.setall(cron_expression)

# 작업을 저장합니다
cron.write()