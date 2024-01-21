import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.daily import DailyTrigger
from apscheduler.jobstores.base import JobLookupError

scheduler = BackgroundScheduler()


def job_function(username):
    print(f"사용자 {username}에 대한 예약 작업이 실행되었습니다.")
    
    # inference_pipeline.py 파일을 실행하는 명령어
    command = f"인퍼런스모델py실행"
    
    try:
        # subprocess를 사용하여 명령어 실행
        subprocess.run(command, shell=True, check=True)
        print("inference_pipeline.py가 성공적으로 실행되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")


def start_scheduler(username, interval, endtime):
    global scheduler, current_username

    # Initialize the scheduler if it's not already initialized
    if scheduler is None:
        initialize_scheduler()

    # Set the current_username
    current_username = username

    end_hour = int(endtime.split(":")[0])
    trigger = DailyTrigger(hour=end_hour)

    # Add the job to the scheduler
    scheduler.add_job(
        job_function,
        args=[username],
        trigger=trigger,
        id=username,
        replace_existing=True,
    )

    # Start the scheduler if not already started
    if not scheduler.running:
        scheduler.start()


def end_scheduler(username):
    try:
        scheduler.remove_job(username)
    except JobLookupError:
        pass
    scheduler.shutdown()


# user_id = "test"
# interval = 10
# endtime = "1:00"
# end_hour = int(endtime.split(":")[0])
# # end_minute = int(endtime.split(":")[1].split(" ")[0])

# cron_job = f"*/{interval} {now_hour}-{end_hour} * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_test.log 2>&1"
# subprocess.run(
#     f'echo "{cron_job}" > /etc/cron.d/cronjob_{user_id}',
#     shell=True,
# )
# print(f'echo "{cron_job}" > /etc/cron.d/cronjob_{user_id}')
