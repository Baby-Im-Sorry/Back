from fastapi import APIRouter, Form, HTTPException, WebSocket, Query
from models import check_user, save_request
from scheduler import start_scheduler, end_scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from models import briefing_collection as bf_collection
from models import request_collection as rq_collection
from bson import ObjectId

router = APIRouter()
scheduler = BackgroundScheduler()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/login")
def login(username: str = Form(...)):
    try:
        result = check_user(username)
        if result["msg"] == "signup":
            return {"message": "signup", "user_id": str(result["user_id"])}
        if result["msg"] == "login":
            return {"message": "login", "user_id": str(result["user_id"])}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Login Error: {str(e)}")


# @router.post("/startBriefing")
# async def startBriefing(
#     username: str = Form(...),
#     interval: str = Form(...),
#     endtime: str = Form(...),
# ):
#     # scheduler의 흐름을 잘 봐야함
#     global scheduler
#     try:
#         interval = int(interval)
#         request_id = save_request(username, interval, endtime)
#         scheduler = start_scheduler(
#             username, interval, endtime, scheduler, request_id, websocket
#         )
#         return {"message": "success", "request_id": str(request_id)}
#     except HTTPException as e:
#         return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str = Query(None),
    interval: str = Query(None),
    endtime: str = Query(None),
):
    await websocket.accept()
    global scheduler
    interval = int(interval)
    request_id = save_request(username, interval, endtime)
    scheduler = await start_scheduler(
        username, interval, endtime, scheduler, request_id, websocket
    )


@router.post("/endBriefing")
def endBriefing(
    username: str = Form(...),
):
    try:
        end_scheduler(username, scheduler)
        return {"message": "success"}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")


@router.get("/getCurrentBriefing")
def getCurrentBriefing(username):
    # 해당 사용자의 가장 최신 request_id 찾기
    latest_request = rq_collection.find_one(
        {"username": username}, sort=[("request_name", -1)]  # -1 : 내림차순 정렬
    )
    # print(latest_request)

    # request_id가 없을 경우 에러 처리
    if not latest_request:
        raise HTTPException(status_code=404, detail="Request not found")
    latest_request_id = latest_request["_id"]
    # print(latest_request_id)
    latest_request_id = ObjectId("65ad4fdc0d7e735ded2fa4be")

    # 해당 request_id를 갖는 모든 briefing 데이터 찾기
    briefings = bf_collection.find({"request_id": latest_request_id})
    # print(briefings)

    # MongoDB cursor를 리스트로 변환 (비동기 방식이라면 async for 사용)
    briefing_list = []
    for briefing in briefings:
        briefing_list.append(briefing["briefing"])
    print(briefing_list)

    # 결과 반환
    return {"message": "success", "content": briefing_list}
