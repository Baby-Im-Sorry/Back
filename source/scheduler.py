import asyncio
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from inference_pipeline import inference_pipeline
from aioscheduler import TimedScheduler


def convert_endtime(endtime_str):
    # 현재 날짜 가져오기
    current_date = datetime.now().date()

    # 시간을 24시간 형식으로 변환 (예: "07:00 PM" -> "19:00")
    endtime_24hr_format = datetime.strptime(endtime_str, "%I:%M %p").time()

    # 현재 날짜와 변환된 시간을 결합
    end_datetime = datetime.combine(current_date, endtime_24hr_format)

    return end_datetime


def sync_inference_pipeline(websocket, request_id):
    asyncio.run(inference_pipeline(websocket, request_id))


async def start_scheduler(
    username, interval, endtime, scheduler, request_id, websocket
):
    # FIXME: APscheduler를 쓰면 비동기 처리가 안됨. 그러나 웹소켓 통신은 비동기 처리가 필요하기 때문에 비동기 처리가 가능한 scheduler를 사용해야함.

    if scheduler is None:
        scheduler = TimedScheduler()

    # TODO: endtime을 Datetime 객체로 변경
    endtime = convert_endtime(endtime)

    if await scheduler.get_job(job_id=username):
        await scheduler.remove_job(job_id=username)

    await scheduler.add_job(
        func=inference_pipeline,
        id=username,
        args=[websocket, request_id],
        trigger="interval",
        minutes=int(interval),
        end_date=endtime,
    )

    # if not scheduler.running:
    #     scheduler.start()

    return scheduler


async def end_scheduler(username, scheduler):
    try:
        await scheduler.remove_job(job_id=username)
    except JobLookupError:
        print("Job does not exist")
    scheduler.shutdown()
