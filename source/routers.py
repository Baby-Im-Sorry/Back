from fastapi import APIRouter, Form, HTTPException, WebSocket, Query
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from models import check_user
from utils import (
    send_briefing_data,
    watch_db,
    get_latest_request,
    new_request,
    endBriefing_worker,
    get_current_breifing,
)

router = APIRouter()
scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)

"""
/login          [post]      (username)
/ws             [websocket] (username, interval, endtime)
/endBriefing    [post]      (username)
"""


@router.post("/login")
def login(username: str = Form(...)):
    logger.info("login()")
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
    logger.info("websocket_endpoint()")
    # 웹소켓 연결
    await websocket.accept()
    # 새 요청 DB에 저장 및 스케쥴러에 등록
    new_request_id = new_request(username, interval, endtime)
    # 웹소켓을 통해 지속적인 업데이트를 front에 날려줌.
    await watch_db(new_request_id, websocket)


# 진행 중 breifing 보기
@router.websocket("/reloadBriefing")
async def reloadBriefing(
    websocket: WebSocket,
    username: str = Query(None),
):
    logger.info("reloadBriefing()")
    await websocket.accept()
    # reloaded된 briefing을 front로 날려줌
    await send_briefing_data(websocket, username)
    request_id = get_latest_request(username)
    await watch_db(request_id, websocket)


@router.post("/endBriefing")
def endBriefing(username: str = Form(...)):
    logger.info("endBriefing()")
    return endBriefing_worker(username)
