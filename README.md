
방구석 브리핑_Backend
================================================

BIS_Backend_Overview
------------------------------------------------

*Implement a functionality using FastAPI to periodically provide clients with briefings on the results of an AI Inference Pipeline. Enable interaction between the client and the server through request and response mechanisms.*

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![WebSocket](https://img.shields.io/badge/WebSocket-4F4F4F?style=for-the-badge&logo=websocket)
![APScheduler](https://img.shields.io/badge/APScheduler-4285F4?style=for-the-badge&logo=apscheduler)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb)

Environment Installation
------------------------
**Please refer to the attached "requirements.txt" for the versions of packages and libraries needed for environment installation.**

### fastapi
```
pip install fastapi
pip install "uvicorn[standard]"
```

### websocket
```
pip install websockets
```

### apscheduler
```
pip install apscheduler
```

### mongodb
```
pip install pymongo
```

Install MongoDB following the instructions on the 

[official MongoDB website](https://www.mongodb.com/try/download/community)



### .env.production
```
pip install python-dotenv
```

Create a separate file named .env.production and add the following content:

```
DATABASE_ID="your_id"
DATABASE_PASSWORD="your_pw"
DATABASE_URI=mongodb+srv://<DATABASE_ID>:<DATABASE_PASSWORD>@"your_dbname".keizkxa.mongodb.net
```

**Ensure that you keep this file secure and do not share sensitive information.**

This file contains configuration details for your production environment, including database credentials. Keep in mind the importance of securing this information and not exposing it publicly.


API List-up
------------

| Index | Method | URI | Description            |
|-------|--------|-----|------------------------|
| 1     | POST   | /login          | 로그인 API              |
| 2     | POST   | /endBriefing    | Briefing 종료          |
| 3     | POST    | /getAllRequest  | 모든 request 조회      |
| 4     | POST    | /getBriefing    | 모든 briefing 조회     |
| 5     | POST    | /aiSummary      | 브리핑 요약            |
| 6     | POST    | /getCustom      | Custom 획득            |
| 7     | POST    | /updateCustom   | Custom 갱신            |
| 8     | POST   | /save_user      | DB 저장 API (User)     |
| 9     | POST   | /save_request   | DB 저장 API (Request)  |
| 10    | POST   | /save_briefing  | DB 저장 API (Briefing) |
| 11    | GET    | /check_user     | DB 조회 API (User)     |
| 12    | PUT    | /update_custom  | DB 조회 API (Custom)   |
| 13    | POST   | /schedule_on    | 스케줄링 on API        |
| 14    | POST   | /schedule_off   | 스케줄링 off API       |
| 15    | WebSocket | /ws           | Web socket (Db 변화 감지)  |
| 16    | WebSocket | /reloadBriefing | Web socket (진행 중 briefing 확인) |

-----------------------

API Specification
-----------------



