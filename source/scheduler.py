from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from inference_pipeline import inference_pipeline

scheduler = BackgroundScheduler()


def start_scheduler(username, interval, endtime, request_id, Websocket):
    if scheduler is None:
        scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=inference_pipeline,
        id=username,
        args=[Websocket, request_id],
        trigger="interval",
        minutes=int(interval),
        end_date=endtime,
    )
    # TODO: endtime을 Datetime 객체로 변경
    # TODO: interval을 파싱해서 시간, 분 단위로 변경

    if not scheduler.running:
        scheduler.start()


def end_scheduler(username):
    try:
        scheduler.remove_job(job_id=username)
    except JobLookupError:
        pass
    scheduler.shutdown()
