# models.py
from pymongo.collection import Collection
from pymongo import MongoClient
import certifi  # mongoDB 보안관련 설정
from dotenv import load_dotenv  # .env 불러오기
import os
import datetime

# .env 파일 로드
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), ".env.production"
)
load_dotenv(dotenv_path)

# MongoDB 연결 설정
DATABASE_URI = os.getenv("DATABASE_URI")
DATABASE_ID = os.getenv("DATABASE_ID")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_URI = DATABASE_URI.replace("<DATABASE_ID>", DATABASE_ID).replace(
    "<DATABASE_PASSWORD>", DATABASE_PASSWORD
)
client = MongoClient(DATABASE_URI, tlsCAFile=certifi.where())  # MongoDB 주소와 포트에 맞게 수정
db = client["BIS"]  # 데이터베이스 이름에 맞게 수정

# user 테이블 불러오기
user_collection: Collection = db["users"]
request_collection: Collection = db["requests"]
breifing_collection: Collection = db["breifings"]


def save_user(username: str):
    user_data = {
        "username": username,
    }
    user_id = user_collection.insert_one(user_data).inserted_id
    return user_id


def save_request(user_id: str, interval: int, endtime: str):
    # request_name: 요청 이름 -> 그날 날짜 시간으로 자동 저장
    request_data = {
        "user_id": user_id,
        "request_name": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "interval": interval,
        "endtime": endtime,
    }
    request_id = request_collection.insert_one(request_data).inserted_id
    return request_id


def save_breifing(request_id: str, breifing: str):
    breifing_data = {
        "request_id": request_id,
        "breifing": breifing,
    }
    breifing_id = breifing_collection.insert_one(breifing_data).inserted_id
    return breifing_id


def check_user(username: str):
    existing_user = user_collection.find_one({"username": username})

    if not existing_user:  # 없는 유저 -> 회원가입
        try:
            user_id = save_user(username)
            return {"msg": "signup", "user_id": str(user_id)}
        except Exception as err:
            return err
    if existing_user:  # 기존 유저 -> 로그인
        return {"msg": "login", "user_id": str(existing_user["_id"])}
