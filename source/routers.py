from fastapi import APIRouter, HTTPException, Form, Query
from models import check_user, save_request
from run_cron import run_cron
from pymongo.collection import Collection
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from config_db import db
import subprocess
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


#docker_path = os.getenv("DOCKER_PATH", "/usr/bin/docker")

@router.post("/endBriefing")
def endBriefing(username: str = Form(...)):
    cronjob_file = f"/etc/cron.d/cronjob_{username}"

    try:
        
        # 조회된 크론 작업에서 해당 사용자의 cronjob 주석 처리
        existing_crontab = subprocess.run(
            ["crontab", "-u", username, "-l"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if existing_crontab.returncode == 0:
            # 만약 crontab이 존재하면 수정
            updated_crontab = existing_crontab.stdout.replace(
                f"/etc/cron.d/cronjob_{username}",
                f"# /etc/cron.d/cronjob_{username}",
            )

            # 주석 처리된 크론 작업을 저장
            subprocess.run(
                ["crontab", "-u", username, "-"],
                input=updated_crontab,
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
        # 크론 작업 파일 삭제
        subprocess.run(["rm", cronjob_file])
        
        return JSONResponse(
            content={"message": "Briefing removed", "username": username}
        )
    except subprocess.CalledProcessError as e:
        return JSONResponse(
            content={"message": "error", "detail": str(e)},
            status_code=500,
        )
    
@router.get("/sendBriefing")    
def sendBriefing(username: str = Query(...)):
    try:
        # MongoDB briefings 컬렉션 조회
        briefings_collection: Collection = db["briefings"]
        briefing_data = list(briefings_collection.find({"username": username}))

        # 조회된 데이터를 JSON 형식으로 반환
        return JSONResponse(content=briefing_data, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error fetching briefing data: {str(e)}")