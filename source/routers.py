from fastapi import APIRouter, WebSocket, HTTPException, Form
from models import check_user, save_request
from run_cron import run_cron
import asyncio
#import subprocess

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


async def endBriefing(ws: WebSocket, username: str):
    await ws.accept()

    cronjob_file = f"/etc/cron.d/cronjob_{username}"

    try:
        # 크론 작업 파일 삭제
        process1 = await asyncio.create_subprocess_exec("rm", cronjob_file)
        await process1.wait()

        # 도커 컨테이너 내부에서 특정 사용자로 로그인하여 크론 작업 등록 취소
        process2 = await asyncio.create_subprocess_exec("docker", "exec", "-u", username, "biscon", "rm", cronjob_file)
        await process2.wait()

        await ws.send_json({"message": "Briefing removed", "username": username})
    except Exception as e:
        await ws.send_json({"message": "error", "detail": str(e)})
    finally:
        await ws.close()