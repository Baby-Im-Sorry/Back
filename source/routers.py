import ast
from fastapi import APIRouter, Form, HTTPException, WebSocket, Query, Response
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import json
from models import check_user, update_custom, get_custom
from pydantic import BaseModel
from utils import (
    send_briefing_data,
    watch_db,
    get_latest_request,
    new_request,
    endBriefing_worker,
    get_current_breifing,
    get_briefing,
    get_all_request,
    chat_summary,
    chat_summary,
)

router = APIRouter()
scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)

"""
/login          [post]      (username)
/ws             [websocket] (username, interval, endtime)
/reloadBriefing [websocket] (username)
/endBriefing    [post]      (username)
/getAllRequest  [post]      (username)
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


@router.post("/getAllRequest")
def getAllRequest(username: str = Form(...)):
    logger.info("getAllRequest()")
    return get_all_request(username)


@router.post("/getBriefing")
def getBriefing(request_id: str = Form(...)):
    logger.info("getBriefing()")
    briefing_list = get_briefing(request_id)
    json_str = json.dumps(briefing_list, ensure_ascii=False)
    return Response(content=json_str, media_type="application/json; charset=UTF-8")


@router.post("/aiSummary")
def aiSummary(request_id: str = Form(...)):
    logger.info("aiSummary")
    # 해당 user의 모든 allrequest -> 전체 request 중 특정 request 내 모든 Briefing
    briefing_data = get_briefing(request_id)
    summary = chat_summary(briefing_data)
    return Response(content=summary, media_type="application/json; charset=UTF-8")


@router.post("/updateCustom")
def updateCustom(username: str = Form(...), custom_list: str = Form(...)):
    logger.info("updateCustom")
    try:
        custom_list = json.loads(custom_list)
        print(f"업데이트커스텀 custom_list : {custom_list}")
        update_custom(username, custom_list)
        return "success to update Custom"
    except Exception as e:
        logger.error(f"Error during update: {e}")
        raise HTTPException(status_code=500, detail="Fail to update Custom")


@router.post("/getCustom")
def getCustom(username: str = Form(...)):
    logger.info("getCustom")
    custom_list = get_custom(username)
    print(f"겟커스텀 custom_list : {custom_list}")
    json_str = json.dumps(custom_list, ensure_ascii=False)
    return Response(content=json_str, media_type="application/json; charset=UTF-8")
