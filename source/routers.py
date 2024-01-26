from fastapi import APIRouter, Form, HTTPException, WebSocket, Query
from apscheduler.schedulers.background import BackgroundScheduler
from models import check_user, request_collection as rq_collection
from scheduler import end_scheduler
from utils import watch_db, get_latest_request, new_request, endBriefing_2, get_current_breifing
from fastapi.websockets import WebSocketDisconnect

router = APIRouter()
scheduler = BackgroundScheduler()

'''
/login          [post]      (username)
/ws             [websocket] (username, interval, endtime)
/endBriefing    [post]      (username)
'''

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


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str = Query(None),
    interval: str = Query(None),
    endtime: str = Query(None),
    ):
    await websocket.accept() # 웹소켓 연결
    # 새 요청 DB에 저장 및 스케쥴러에 등록
    new_request_id = new_request(username, interval, endtime)
    # 웹소켓을 통해 지속적인 업데이트를 front에 날려줌.
    await watch_db(new_request_id, websocket)


#진행 중 breifing 보기
@router.websocket("/reloadBriefing")
async def reloadBriefing(
    websocket: WebSocket,
    username: str = Query(None),
):
    await websocket.accept()  
    #reloaded된 briefing을 front로 날려줌 
    await send_briefing_data(websocket, username)


# db를 불러온 후 front로 보내기
async def send_briefing_data(websocket: WebSocket, username: str):
    try:
        while True:
            briefing_data = get_current_breifing(username)
            if briefing_data is not None:
                await websocket.send_json({"briefing_data": briefing_data})
    except WebSocketDisconnect:
        pass
    


@router.post("/endBriefing")
def endBriefing(username: str = Form(...)):
    latest_request_id = get_latest_request(username)
    # 로직 추가해야함..