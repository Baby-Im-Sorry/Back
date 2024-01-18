from fastapi import APIRouter, WebSocket, HTTPException, Form
from models import check_user, save_request
from run_cron import run_cron
import subprocess
from fastapi.responses import JSONResponse
import os

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello!! World"}


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


docker_path = os.getenv("DOCKER_PATH", "/usr/bin/docker")

@router.post("/endBriefing")
def endBriefing(username: str = Form(...)):
    cronjob_file = f"/etc/cron.d/cronjob_{username}"

    try:
       
        # 크론 작업 파일 삭제
        subprocess.run(["rm", cronjob_file])
        # docker container 내부에서 특정 사용자로 로그인 해 크론 작업 등록 취소 
        # subprocess.run(["docker", "exec", "-u", username, "biscon", "rm", cronjob_file])

        return JSONResponse(content={"message": "Briefing removed", "username": username})
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"message": "error", "detail": str(e)}, status_code=500)