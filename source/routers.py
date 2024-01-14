from fastapi import APIRouter, Form, HTTPException
from models import check_user, save_request
from run_cron import run_cron
import subprocess

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
        run_cron(username, interval, endtime)
        # 위에건 크론 등록
        return {"message": "success", "request_id": str(request_id)}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Briefing Error: {str(e)}")

@router.post("/endBriefing")
def endBriefing(
    username: str = Form(...)
):
    try:
        #등록된 크론job파일 삭제
        subprocess.run(["crontab", "-r", "-u", username], check=True)
        return {"message": "Briefing remove", "username": username}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Briefing 에러: {str(e)}")



# @router.post("/sendclient")
# def send_to_client():
#     pass
