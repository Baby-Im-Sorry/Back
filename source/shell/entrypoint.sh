#!/bin/bash

# 크론 시작
cron

# Uvicorn 서버 시작
exec uvicorn main:app --reload --host 0.0.0.0 --port 8000
