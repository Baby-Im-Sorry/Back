# 베이스 이미지로 Python 이미지 사용
FROM python:3.12

# 필요한 Python 패키지 설치 (pip freeze > requirements.txt 명령을 통해 requirements.txt를 갱신해주는 작업이 선수로 필요)
COPY . /bis/
RUN pip install -r /bis/requirements.txt

# 컨테이너의 작업 디렉터리 설정 (쉘이 초기에 bis 폴더에서 열림)
WORKDIR /bis

# 컨테이너가 시작될 때 main.py 실행
CMD ["uvicorn", "source.main:app", "--reload"]