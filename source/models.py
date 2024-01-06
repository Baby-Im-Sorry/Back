from pymongo.collection import Collection
from pymongo import MongoClient
import certifi # mongoDB 보안관련 설정

#mongoDB 연결 설정
client = MongoClient("mongodb+srv://BIS:<password>@biscluster.keizkxa.mongodb.net/?authMechanism=DEFAULT", tlsCAFile=certifi.where())  # MongoDB 주소와 포트에 맞게 수정
db = client["test"]  # 데이터베이스 이름에 맞게 수정

user_collection: Collection = db["users"]

def create_user(username: str):
    user_data = {
        "username": username,
    }
    user_id = user_collection.insert_one(user_data).inserted_id
    return user_id

def check_user(username: str):
    existing_user = user_collection.find_one({"username": username})

    if not existing_user: # 없는 유저 -> 회원가입
        try:
            user_id = create_user(username)
            return {"msg": "signup", "user_id": str(user_id)}
        except Exception as err:
            return err
    if existing_user: # 기존 유저 -> 로그인
        return {"msg": "login", "user_id": str(existing_user["_id"])}
