from fastapi import APIRouter, HTTPException, Form, Query
from models import check_user, save_request
from run_cron import run_cron
from pymongo.collection import Collection
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from config_db import db
import subprocess
import logging
#import os


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
        # 로깅
        logging.info(f"사용자 {username}의 cronjob을 제거하는 중")

        # 지정된 사용자에 대한 crontab이 있는지 확인
        existing_crontab = subprocess.run(
            ["crontab", "-u", username, "-l"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if existing_crontab.returncode == 0:
            # crontab이 존재하면 수정
            updated_crontab = existing_crontab.stdout.replace(
                f"/etc/cron.d/cronjob_{username}",
                f"# /etc/cron.d/cronjob_{username}",
            )

            # 주석 처리된 crontab을 저장
            subprocess.run(
                ["crontab", "-u", username, "-"],
                input=updated_crontab,
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
            logging.info("Crontab이 성공적으로 수정되었습니다.")

        # cronjob 파일 제거
        subprocess.run(["rm", cronjob_file])

        # 로깅
        logging.info(f"Cronjob 파일 {cronjob_file}이 제거되었습니다.")

        return JSONResponse(
            content={"message": "Briefing removed", "username": username}
        )
    except subprocess.CalledProcessError as e:
        # 로깅
        logging.error(f"에러: {str(e)}")

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