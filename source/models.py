from pymongo.collection import Collection
from config_db import db

#user 테이블 불러오기
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
