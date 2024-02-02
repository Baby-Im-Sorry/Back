from pymongo.collection import Collection
from config_db import db
import datetime
import logging

# user 테이블 불러오기
user_collection: Collection = db["users"]
request_collection: Collection = db["requests"]
briefing_collection: Collection = db["briefings"]

logger = logging.getLogger(__name__)

def save_user(username: str):
    logger.info("save_user()")
    user_schema = {
        "username": username,
        "custom": []
    }
    user_id = user_collection.insert_one(user_schema).inserted_id
    return user_id


def save_request(username: str, interval: int, endtime: str):
    logger.info("save_request()")
    # request_name: 요청 이름 -> 그날 날짜 시간으로 자동 저장
    parsed_time = datetime.datetime.strptime(endtime, "%I:%M %p")
    endtime = parsed_time.strftime("%H:%M")
    request_schema = {
        "username": username,
        "request_name": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "interval": interval,
        "endtime": endtime,
        "is_active": True,
    }
    request_id = request_collection.insert_one(request_schema).inserted_id
    return request_id


def save_briefing(request_id: str, briefing: str):
    logger.info("save_briefing()")
    briefing_schema = {
        "request_id": request_id,
        "briefing": briefing,
    }
    briefing_id = briefing_collection.insert_one(briefing_schema).inserted_id
    return briefing_id

def check_user(username: str):
    logger.info("check_user()")
    existing_user = user_collection.find_one({"username": username})

    if not existing_user:  # 없는 유저 -> 회원가입
        try:
            user_id = save_user(username)
            return {"msg": "signup", "user_id": str(user_id)}
        except Exception as err:
            return err
    if existing_user:  # 기존 유저 -> 로그인
        return {"msg": "login", "user_id": str(existing_user["_id"])}

# user 테이블의 custom 필드 업데이트
def update_custom(username: str, custom_list: list):
    logger.info("update_custom()")
    user_collection.update_one(
        {"username": username},
        {"$set": {"custom": custom_list}}   # 기존 value 값 덮어쓰기
    )
    return None

def get_custom(username: str):
    logger.info("get_custom()")
    user = user_collection.find_one({"username": username})
    custom_list = user['custom']
    return custom_list