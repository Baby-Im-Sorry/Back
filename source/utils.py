from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import HTTPException
from models import save_request
from scheduler import start_scheduler, end_scheduler
from models import request_collection as rq_collection, briefing_collection as bf_collection
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from config_db import DATABASE_URI
from bson import ObjectId

scheduler = BackgroundScheduler()

# 기존 브리핑 종료 & 새 요청 등록
def new_request(username, interval, endtime):
    stop_active_breifing(username) # 진행중인 브리핑 종료
    # DB에 request 저장 및 스케쥴러에 작업 등록
    global scheduler
    interval = int(interval)
    request_id = save_request(username, interval, endtime, is_active=True)
    scheduler = start_scheduler(username, interval, endtime, scheduler, request_id)
    return request_id
    

# 진행중인 브리핑 있는지 확인 후, 종료
def stop_active_breifing(username):
    latest_request_id = get_latest_request(username)
    if latest_request_id != None:
        is_active = rq_collection.find_one({"_id": latest_request_id})["is_active"]
        if is_active:
<<<<<<< Updated upstream
            endBriefing2(username, latest_request_id)


# 특정 request의 is_active 를 false로 바꾸고, 스케쥴러에서도 삭제
def endBriefing2(username, request_id):
=======
            endBriefing_2(username, latest_request_id)


# 특정 request의 is_active 를 false로 바꾸고, 스케쥴러에서도 삭제
def endBriefing_2(username, request_id):
>>>>>>> Stashed changes
    rq_collection.update_one({"_id": request_id}, {"$set": {"is_active": False}})
    try:
        end_scheduler(username, scheduler)
        print('스케쥴러에서 해당 request 삭제 성공')
        return {"message": "success"}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")




async def watch_db(request_id, websocket):
    # motor 이용해서 비동기로 mongoDB 접근
    client = AsyncIOMotorClient(DATABASE_URI)
    db = client.BIS
    bf_collection2 = db.briefings
    
    try:
        pipeline = [{"$match": {"fullDocument.request_id": ObjectId(request_id)}}]
        change_stream = bf_collection2.watch(pipeline)
        async for change in change_stream:
            new_data = change["fullDocument"]["briefing"]
            await websocket.send_text(f'{new_data}')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await change_stream.close()
        await websocket.close()


# 해당 사용자의 가장 최신 request_id 찾기
def get_latest_request(username):
    latest_request = rq_collection.find_one(
        {"username": username}, sort=[("request_name", -1)]  # -1 : 내림차순 정렬
    )
    if latest_request == None:
        return None
    return ObjectId(latest_request["_id"])


# 해당 사용자의 db내역 불러오기
def get_current_breifing(username):
    latest_request_id = get_latest_request(username)
    reloading_db = bf_collection.find_one(latest_request_id["briefing"])
    if reloading_db == None:
        return None
    return reloading_db

