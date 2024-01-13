from fastapi import APIRouter, Form, HTTPException
from models import check_user, save_request
from test import test

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


@router.post("/startBreifing")
def startBriefing(
    user_id: str = Form(...),
    interval: int = Form(...),
    endtime: str = Form(...),
):
    try:
        request_id = save_request(user_id, interval, endtime)
        test.test(user_id, interval, endtime)
        # 위에건 크론 등록
        return {"message": "success", "request_id": str(request_id)}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Breifing Error: {str(e)}")


# @router.post("/sendclient")
# def send_to_client():
#     pass
