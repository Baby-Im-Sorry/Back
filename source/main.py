from fastapi import FastAPI # fastapi 클래스를 불러옵니다. 
from typing import Union
from pydantic import BaseModel # 데이터 직렬화를 위한 라이브러리
from getDB import create_user, get_user
app = FastAPI() # FastAPI 객체 생성

@app.get("/") # get 요청을 할 url
async def root(): # root() 함수를 실행하고
    return {"message": "Hello World"} # Hello World란 메시지 반환합니다.

'''
127.0.0.1/items/5?q=안녕
위 ulr로 접속하면 item_id 변수에 5가 q에 안녕이 저장돼서 {"item_id": 5, "q": "안녕"} 가 client로 전송됨.
q: Union[str, None] = None  #인자인 q에 str 또는 None 타입이 들어가는데, default로 None이 설정됨 (q값이 안 들어오는 경우)
'''
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

from fastapi import FastAPI, HTTPException
from pymongo.collection import Collection
from model import db

# user 테이블 불러오기
user_collection: Collection = db["users"]

# 사용자 생성
@app.post("/create/")
def create_user(username: str):
    # 중복 사용자 확인
    existing_user = user_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # 중복이 없을 때 사용자 생성
    user_data = {
        "username": username,
    }
    user_id = user_collection.insert_one(user_data).inserted_id
    return {"message": "User created successfully", "user_id": str(user_id)}

# 사용자 조회
@app.get("/get/{username}")
def get_user(username: str):
    user = user_collection.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])  # ObjectId를 문자열로 변환
        return user
    raise HTTPException(status_code=404, detail="User not found")

