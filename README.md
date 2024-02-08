
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
| 2    | WebSocket | /ws           | Web socket (Db 변화 감지)  |
| 3    | WebSocket | /reloadBriefing | Web socket (진행 중 briefing 확인) |
| 4     | POST   | /endBriefing    | Briefing 종료          |
| 5     | POST    | /getAllRequest  | 모든 request 조회      |
| 6     | POST    | /getBriefing    | 모든 briefing 조회     |
| 7     | POST    | /aiSummary      | 브리핑 요약            |
| 8     | POST    | /getCustom      | Custom 획득            |
| 9     | POST    | /updateCustom   | Custom 갱신            |


-----------------------

API Specification
-----------------


* login

-----------------
| Endpoint      | Method |
|---------------|--------|
| `POST /login` | POST   |
-----------------

    * description
    # check_user in models.py 를 이용해 신규 회원, #기존 회원 검사. 
    #기존 회원인 경우 "message":"signup"과 함께 #user_id 반환
    #신규 회원인 경우 "message":"login"과 함께 
    #user_id 반환

    -------------------
    | **Header**       ||
    |------------------||
    | `Content-Type`   ||
    |   `application/x-www-form-urlencoded` ||
    -------------------

    -------------------
    | **Body**         ||
    |------------------||
    | Parameter  | Type   | Description         |
    |-----------|--------|---------------------|
    | username  | string | User's username.    |
    -------------------

    ** Response **
    -------------------
    | **Success Response**  |||
    |----------------------|||
    | **Status Code:** 200 OK ||
    | **Body:**             ||
    | ```json             |||
    | {                    |||
    |   "message": "signup",||
    |   "user_id": "user_id_value" ||
    | }                    |||
    | ```                  |||
    | or                   |||
    | ```json             |||
    | {                    |||
    |   "message": "login", ||
    |   "user_id": "user_id_value" ||
    | }                    |||
    | ```                  |||
    ----------------------

    -------------------
    | **Error Response**    |||
    |----------------------|||
    | **Status Code:** 500 Internal Server Error ||
    | **Body:**             ||
    | ```json             |||
    | {                    |||
    |   "detail": "Login Error: error_message" ||
    | }                    |||
    | ```                  |||
    -------------------

