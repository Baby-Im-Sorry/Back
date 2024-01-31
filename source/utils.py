from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import HTTPException
from models import save_request
from scheduler import start_scheduler, end_scheduler
from models import (
    request_collection as rq_collection,
    briefing_collection as bf_collection,
)
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from config_db import DATABASE_URI
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


# 해당 사용자의 가장 최신 request_id 찾기
def get_latest_request(username):
    logger.info("get_latest_request()")
    latest_request = rq_collection.find_one(
        {"username": username}, sort=[("request_name", -1)]  # -1 : 내림차순 정렬
    )
    if latest_request == None:
        return None
    return latest_request["_id"]


# 특정 request의 is_active 를 false로 바꾸고, 스케쥴러에서도 삭제
def endBriefing_worker(username):
    logger.info("endBriefing_worker()")
    latest_request_id = get_latest_request(username)
    rq_collection.update_one(
        {"_id": ObjectId(latest_request_id)}, {"$set": {"is_active": False}}
    )
    try:
        end_scheduler(username, scheduler)
        print("스케쥴러에서 해당 request 삭제 성공")
        return {"message": "브리핑 성공적으로 종료"}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")


# 진행중인 브리핑 있는지 확인 후, 종료
def stop_active_breifing(username):
    logger.info("stop_active_breifing()")
    latest_request_id = get_latest_request(username)
    if latest_request_id != None:
        is_active = rq_collection.find_one({"_id": ObjectId(latest_request_id)})[
            "is_active"
        ]
        if is_active:
            endBriefing_worker(username)


# 기존 브리핑 종료 & 새 요청 등록
def new_request(username, interval, endtime):
    logger.info("new_request()")
    stop_active_breifing(username)  # 진행중인 브리핑 종료
    # DB에 request 저장 및 스케쥴러에 작업 등록
    global scheduler
    interval = int(interval)
    request_id = save_request(username, interval, endtime, is_active=True)
    scheduler = start_scheduler(username, interval, endtime, scheduler, request_id)
    return request_id


async def watch_db(request_id, websocket):
    logger.info("watch_db()")
    # motor 이용해서 비동기로 mongoDB 접근
    client = AsyncIOMotorClient(DATABASE_URI)
    db = client.BIS
    try:
        pipeline = [{"$match": {"fullDocument.request_id": ObjectId(request_id)}}]
        change_stream = db.briefings.watch(pipeline)
        async for change in change_stream:
            new_data = change["fullDocument"]["briefing"]
            await websocket.send_text(f"{new_data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await change_stream.close()
        await websocket.close()

# DB에서 briefing 조회 후 front로 보내기
async def send_briefing_data(websocket, username: str):
    logger.info("send_briefing_data()")
    briefing_data = get_current_breifing(username)
    if briefing_data is not None:
        await websocket.send_json({"briefing_data": briefing_data})


# DB 조회하기 (모든 briefing 데이터 조회)
def get_briefing(request_id):
    logger.info("get_briefing()")
    try: 
        briefings = bf_collection.find({"request_id": ObjectId(request_id)})
        briefing_list = [briefing.get("briefing") for briefing in briefings] # bf_collection 의 briefing 필드만 추출
        return briefing_list
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")


# 해당 사용자의 db내역 불러오기
def get_current_breifing(username):
    logger.info("get_current_breifing()")
    latest_request_id = get_latest_request(username) # 사용자의 가장 최근 request
    briefing_data = get_briefing(latest_request_id) # 해당 request의 모든 briefing 데이터 조회
    return briefing_data

# 사용자의 모든 request 불러오기
def get_all_request(username):
    logger.info("get_all_request()")
    # request_id, request_name, endtime 필드만 추출
    all_request = rq_collection.find(
        {"username": username},
        {"_id": 1, "request_name": 1, "endtime": 1}
    )
    # 리스트에 담기
    request_list = [
        {"request_id": str(request.get("_id")),
        "request_name": request.get("request_name"), 
        "endtime": request.get("endtime")}
        for request in all_request
    ]
    request_list.reverse()  # 내림차순 정렬
    return request_list