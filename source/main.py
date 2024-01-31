from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
import logging

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

logging.basicConfig(level=logging.INFO) # 로그