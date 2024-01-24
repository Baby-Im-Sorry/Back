from fastapi import APIRouter, Form, HTTPException, WebSocket, Query
from models import check_user, save_request
from scheduler import start_scheduler, end_scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from models import briefing_collection as bf_collection
from models import request_collection as rq_collection
from bson import ObjectId

router = APIRouter()
scheduler = BackgroundScheduler()

websocket_list = []

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


def new_request(username, interval, endtime):
    global scheduler
    interval = int(interval)
    request_id = save_request(username, interval, endtime, is_active=True)
    # 스케쥴러에 작업 등록
    scheduler = start_scheduler(username, interval, endtime, scheduler, request_id)
    return request_id


async def watch_db(request_id, websocket):
    print("req_id: ", request_id)
    if request_id != None:
        # Change Streams 파이프라인 설정: 특정 request_id를 갖는 새로운 문서만 감지
        try:
            pipeline = [{"$match": {"fullDocument.request_id": ObjectId(request_id)}}]
            change_stream = bf_collection.watch(pipeline)
            while True:
                change = next(change_stream)
                # 새로 추가된 데이터의 내용을 웹소켓을 통해 전송
                print("newdata : ------------------------")
                new_data = change["fullDocument"]["briefing"]
                print(new_data)
                await websocket.send_text(f"새로운 데이터 추가됨: {new_data}")
                is_stop = await websocket.receive_text()
                if is_stop == 'True':
                    websocket.close()
                print("keep going")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await websocket.close()


# DB 감지 코드 (앱 실행 중일 때)
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str = Query(None),
    interval: str = Query(None),
    endtime: str = Query(None),
):
    await websocket.accept()
    websocket_list.append(websocket)
    latest_request_id = get_latest_request(username)

    if latest_request_id != None:
        # request_id의 is_active 확인
        is_active = rq_collection.find_one({"_id": latest_request_id})["is_active"]
        if is_active:  # 진행중인 브리핑이 있다면, 종료
            endBriefing(username)
    # 새로운 요청 생성
    new_request_id = new_request(username, interval, endtime)
    # 웹소켓을 통해 지속적인 업데이트를 front에 날려줌.
    await watch_db(new_request_id, websocket)


# 재접속할 때 DB 불러오기
# @router.get("/getCurrentBriefing")
# async def getCurrentBriefing(username):
# latest_request_id = get_latest_request(username)
# if latest_request_id:
#     # request_id의 is_active 확인
#     is_active = rq_collection.find_one({"_id": latest_request_id})["is_active"]
#     if is_active: # 진행중인 브리핑이 있다면, 해당 request_id를 갖는 모든 briefing 데이터 찾기
#         briefings = bf_collection.find({"request_id": latest_request_id})
#         # MongoDB cursor를 리스트로 변환 (비동기 방식이라면 async for 사용)
#         briefing_list = []
#         for briefing in briefings:
#             briefing_list.append(briefing["briefing"])
#         print(briefing_list)
#         # 결과 반환 & 웹소켓을 통해 지속적인 업데이트를 front 에 날려줌.
#         await watch_db(latest_request_id, websocket)
#         return {"message": "success", "content": briefing_list}
#     else:
#         return {"message": "No 'active' request running.", "content": None}
# return {"getCurrentBriefing"}


# 해당 사용자의 가장 최신 request_id 찾기
def get_latest_request(username):
    latest_request = rq_collection.find_one(
        {"username": username}, sort=[("request_name", -1)]  # -1 : 내림차순 정렬
    )
    if latest_request == None:
        return None
    return ObjectId(latest_request["_id"])

@router.websocket("/endBriefing")

@router.post("/endBriefing")
def endBriefing(username: str = Form(...)):
    websocket_list[0] #몇번째가 누구건지 어케 아냐.
    #list 자료구조가 아닌 dict을 사용해서 key에는 username을 value엔 websocket 객체를.
    # await websocket.close()
    latest_request_id = get_latest_request(username)
    rq_collection.update_one({"_id": latest_request_id}, {"$set": {"is_active": False}})
    try:
        end_scheduler(username, scheduler)
        return {"message": "success"}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")