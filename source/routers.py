from fastapi import APIRouter, HTTPException
from models import check_user

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/login/{username}")
def login(username: str):
    try:
        result = check_user(username)
        if result["msg"] == "signup": # 새 유저 생성됨
            return {"message": "signup", "user_id": str(result["user_id"])}
        if result["msg"] == "login": # 기존 유저 로그인
            return {"message": "login", "user_id": str(result["user_id"])}
    except HTTPException as e:
        return HTTPException(status_code=500, detail=f"Login Error: {str(e)}")
