from fastapi import APIRouter, Form, HTTPException, WebSocket
from models import check_user, save_request
from run_cron import start_cron
from models import briefing_collection as bf_collection

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/login")
def login(username: str = Form(...)):
    try:
        result = check_user(username)
        if result["msg"] == "signup":  # 새 유저 생성됨
            return {"message": "signup", "user_id": str(result["user_id"])}
        if result["msg"] == "login":  # 기존 유저 로그인
            return {"message": "login", "user_id": str(result["user_id"])}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Login Error: {str(e)}")


@router.post("/startBriefing")
def startBriefing(
    username: str = Form(...),
    interval: str = Form(...),
    endtime: str = Form(...),
):
    try:
        interval = int(interval)
        request_id = save_request(username, interval, endtime)
        start_cron(username, interval, endtime)
        return {"message": "success", "request_id": str(request_id)}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    change_stream = bf_collection.watch()
    try:
        while True:
            change = next(change_stream)
            # MongoDB에서 변경사항이 감지되면 메시지 전송
            await websocket.send_text("변화 감지!")
    except Exception as e:
        print(f"Error: {e}")
    # finally:
    # await websocket.close()
