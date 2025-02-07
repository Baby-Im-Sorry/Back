
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


* ### login

    * description
        
        * Utilize **check_user** in **models.py** to verify new and existing users.

            * In the case of an existing user, return `{"message": "signup", "user_id": <user_id>}`.
            * For a new user, return `{"message": "login", "user_id": <user_id>}`.

| **Endpoint** | **Method** |
|--------------|------------|
| `POST /login`| POST       |


|  |**Request**|
|--------------|------------------|
| **Header**   ||
| *"No special headers required"* ||
| **Body**     ||
| *Parameter*    | *Type* ||
| username    | String || 
  
|**Response** |
|--------------|
| **1) Success Response** |
| **Status Code:** 200 OK |
| **Body:** |
| ```json { "message" : "signup", "user_id" : "user_id_value"} ```|
| or |
| ```json { "message" : "login", "user_id" : "user_id_value"} ```|
| **2) Error Response** |
| **Status Code:** 500 Internal Server Error |
| **Body:** |
| ```json { "detail": "Login Error: error_message"} ```|




* ### websocket_endpoint

    * Description:
        * Handle WebSocket connections for continuous updates.
        * Establish WebSocket connection.
        * Store new request in the database and register with the scheduler.
        * Continuously send updates to the frontend through the WebSocket.
  

| **Endpoint** | **Method** |
|--------------|------------|
| `websocket/ws`| WebSocket |


**Parameters**

| **Name**     | **Type**  | **Description**                   |
|--------------|-----------|-----------------------------------|
| websocket    | WebSocket | The WebSocket connection object.  |
| username     | String    | User's username.                  |
| interval     | String    | Requested interval for updates.   |
| endtime      | String    | Requested end time for updates.   |




* ### websocket_reloadBriefing

    * Description
        * Display the ongoing briefing.
        * Establish WebSocket connection.
        * Send reloaded briefing data to the frontend.
        * Get the latest request ID and continuously watch the database for updates.
    
| **Endpoint** | **Method** |
|--------------|------------|
| `websocket/reloadBriefing`| WebSocket |


    
 **Parameters**
| **Name**     | **Type**  | **Description**                 |
|--------------|-----------|---------------------------------|
| websocket    | WebSocket | The WebSocket connection object. |
| username     | String    | User's username.                 |

* ### endBriefing

    * description
        * Terminate the ongoing briefing.
        * The function **endBriefing** uses the **endBriefing_worker** from **utils.py** and **end_scheduler** from **scheduler.py**.

            * Upon success, it prints a success message and returns a success response with the message `"Briefing successfully terminated"`.
            * In case of failure (e.g., an `exception`), it catches the `"HTTPException"`, logs the error message, and returns an error response with the corresponding status code and details.

| **Endpoint** | **Method** |
|--------------|------------|
| `POST /endBriefing`| POST       |


|  |**Request**|
|--------------|------------------|
| **Header**   ||
| *"No special headers required"* ||
| **Body**     ||
| *Parameter*    | *Type* ||
| username    | String || 
  
|**Response** |
|--------------|
| **1) Success Response** |
| **Status Code:** 200 OK |
| **Body:** |
| ```"message": "브리핑 성공적으로 종료" ```|
| **2)Error Response** |
| **Status Code:** 500 Internal Server Error |
| **Body:** |
| ```Internal Server Error ```|

* ### getAllRequest

    * description
        * Implement a functionality to retrieve all requests for a specific username from the `"request" Collection` within the database.
        * **getAllRequest** utilizes the **get_all_request** function from **utils.py** to retrieve and return the list of requests for a specific username from the **"request" Collection** in the database.

* ### getBriefing

    * description
        * Retrieve briefing information based on the provided `request_id`.
        * Utilize the `get_briefing` function from `utils.py` to perform a functionality that retrieves all briefings for a specific request_id from the `"briefing" Collection` in the database.

* ### aiSummary

    * description
        * Generates an AI summary captions based on the provided `request_id`.
        * This API utilizes two methods: `get_briefing` in `utils.py` for querying all data from the database and `chat_summary` in `utils.py` for generating AI summaries based on the returned briefing data list.

        * To provide additional details on `chat_summary`, it involves using the `OpenAI API key` to generate messages based on a specified format prompt. This process utilizes the `GPT-4-preview model` and performs `prompt engineering` on the briefing data list retrieved earlier, adjusting hyperparameters such as `"tone, writing style, temperature, top_p,"` and others.

* ### getCustom

    * description
        * this API retrieves the `"custom"` data for a specific username. The obtained `custom_list` is then used to generate an HTTP response in JSON format, encoded in UTF-8.
        * The `get_custom` in `models.py` process involves searching for the specified username within the "user" collection in the database and referring to it as a custom list.


* ### updateCustom

    * description
        * Utilizing the `update_custom` function in `models.py`, this API updates the `"custom"` field in the "user" table.
            * If the custom_list is successfully updated, it returns the message `"Success to update Custom."`
            * In case of exceptions or errors, it raises an `HTTPException` with a status code of 500 and the detail `"Fail to update Custom."`



