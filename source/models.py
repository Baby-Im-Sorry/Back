from pymongo.collection import Collection
from config_db import db
from mongoengine import connect, Document, StringField

connect("test")

#user 테이블 불러오기
user_collection: Collection = db["users"]

class User(Document):
    username = StringField(required=True, unique=True)

def create_user(req_name: str):
    new_user = User(username=req_name)
    user_id = new_user.save().id
    return user_id

def check_user(req_name: str):
    existing_user = User.objects(username=req_name).first()
    if not existing_user: # 없는 유저 -> 회원가입
        try:
            user_id = create_user(req_name)
            return {"msg": "signup", "user_id": str(user_id)}
        except Exception as err:
            return err
    if existing_user: # 기존 유저 -> 로그인
        return {"msg": "login", "user_id": str(existing_user.id)}
