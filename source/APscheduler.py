import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

scheduler = BackgroundScheduler()
scheduler.start()

def my_job():
    # 작업 로직
    result = "작업 결과"
    logging.info(f"My job result: {result}")

job1 = scheduler.add_job(my_job, 'interval', seconds=10)
job2 = scheduler.add_job(my_job, 'interval', minutes=30)

# Listing jobs
jobs = scheduler.get_jobs()
for job in jobs:
    logging.info(f"Job ID: {job.id}, Next run time: {job.next_run_time}, Trigger: {job.trigger}")

# Removing a job
scheduler.remove_job(job2.id)

logging.info('---------------')

jobs = scheduler.get_jobs()
for job in jobs:
    logging.info(f"Job ID: {job.id}, Next run time: {job.next_run_time}, Trigger: {job.trigger}")

# 스케줄러 종료 전 대기 (추가된 부분)
try:
    # 이 부분은 스크립트가 바로 종료되지 않도록 대기 상태를 유지합니다.
    # 실제 환경에서는 서버와 같은 지속적인 서비스에서는 필요하지 않을 수 있습니다.
    import time
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # 스크립트 종료 시 스케줄러도 함께 종료
    scheduler.shutdown()
