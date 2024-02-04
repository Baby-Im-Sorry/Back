import asyncio
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from inference_pipeline import inference_pipeline


def convert_endtime(endtime_str):
    current_date = datetime.now().date()
    endtime_str = endtime_str.replace("%20", " ")
    endtime_24hr_format = datetime.strptime(endtime_str, "%I:%M %p").time()
    end_datetime = datetime.combine(current_date, endtime_24hr_format)

    return end_datetime


def start_scheduler(username, interval, endtime, scheduler, request_id):
    if scheduler is None:
        scheduler = BackgroundScheduler()
    endtime = convert_endtime(endtime)
    if scheduler.get_job(job_id=username):
        scheduler.remove_job(job_id=username)
    scheduler.add_job(
        func=inference_pipeline,
        id=username,
        args=[username, request_id],
        trigger="interval",
        # minutes=int(interval),
        seconds=int(interval),
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
