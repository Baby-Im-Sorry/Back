from pymongo import MongoClient
import certifi  # mongoDB 보안관련 설정
from dotenv import load_dotenv  # .env 불러오기
import os

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
