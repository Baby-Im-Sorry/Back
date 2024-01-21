from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from inference_pipeline import inference_pipeline


def convert_endtime(endtime_str):
    # 현재 날짜 가져오기
    current_date = datetime.now().date()

    # 시간을 24시간 형식으로 변환 (예: "07:00 PM" -> "19:00")
    endtime_24hr_format = datetime.strptime(endtime_str, "%I:%M %p").time()

    # 현재 날짜와 변환된 시간을 결합
    end_datetime = datetime.combine(current_date, endtime_24hr_format)

    return end_datetime


def start_scheduler(username, interval, endtime, request_id, Websocket):
    if scheduler is None:
        scheduler = BackgroundScheduler()

    # TODO: endtime을 Datetime 객체로 변경
    endtime = convert_endtime(endtime)

    scheduler.add_job(
        func=inference_pipeline,
        id=username,
        args=[Websocket, request_id],
        trigger="interval",
        minutes=int(interval),
        end_date=endtime,
    )

    if not scheduler.running:
        scheduler.start()

    return scheduler


def end_scheduler(username, scheduler):
    try:
        scheduler.remove_job(job_id=username)
    except JobLookupError:
        print("Job does not exist")
    scheduler.shutdown()
