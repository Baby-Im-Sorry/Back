from fastapi import APIRouter, Form, HTTPException, WebSocket
from models import check_user, save_request
from run_cron import start_cron, end_cron
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


@router.post("/endBriefing")
def endBriefing(
    username: str = Form(...),
):
    try:
        end_cron(username)
        return {"message": "success"}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")

# 웹소켓 라우터
@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()

    # 해당 사용자의 가장 최신 request_id 찾기
    latest_request = bf_collection.request.find_one( ###
        {"username": username},
        sort=[("request_id", -1)] # -1 : 내림차순 정렬
    )
    # requset_id가 없을 경우 에러 처리
    latest_request_id = latest_request["request_id"] if latest_request else None 

    # Change Streams 파이프라인 설정
    if latest_request_id:
         # Change Streams 파이프라인 설정: 특정 request_id를 갖는 새로운 문서만 감지
        pipeline = [
            {"$match": {
                "operationType": "insert",
                "fullDocument.request_id": latest_request_id
            }}
        ]
        change_stream = bf_collection.watch(pipeline)

        try:
            while True:
                change = next(change_stream)
                # 새로 추가된 데이터의 내용을 웹소켓을 통해 전송
                new_data = change["fullDocument"]
                print('------------------------')
                print(new_data)
                await websocket.send_text(f"새로운 데이터 추가됨: {new_data}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await websocket.close()