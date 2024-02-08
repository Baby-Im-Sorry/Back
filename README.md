
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

##### fastapi
```
pip install fastapi
pip install "uvicorn[standard]"
```

##### websocket
```
pip install websockets
```

##### apscheduler
```
pip install apscheduler
```

##### mongodb
```
pip install pymongo
```

Install MongoDB following the instructions on the [official MongoDB website][mongodb][mongodb]: https://www.mongodb.com/try/download/community


* .env.production
```
pip install python-dotenv
```

Create a separate file named .env.production and add the following content:

```
DATABASE_ID="your_id"
DATABASE_PASSWORD="your_pw"
DATABASE_URI=mongodb+srv://<DATABASE_ID>:<DATABASE_PASSWORD>@"your_dbname".keizkxa.mongodb.net
```

Ensure that you keep this file secure and do not share sensitive information.
This file contains configuration details for your production environment, including database credentials. Keep in mind the importance of securing this information and not exposing it publicly.


