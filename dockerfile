# 베이스 이미지로 Python 이미지 사용
FROM python:3.9

# 로컬에 있는 파일을 이미지에 복사하기
COPY requirements.txt /bis/
COPY .env.production /bis/
COPY source/*.py /bis/source/

# 필요한 Python 패키지 설치 (pip freeze > requirements.txt 명령을 통해 requirements.txt를 갱신해주는 작업이 선수로 필요)
RUN pip install -r /bis/requirements.txt
RUN apt-get update && apt-get install -y cron && apt-get install -y vim

# 컨테이너의 작업 디렉터리 설정 (쉘이 초기에 bis 폴더에서 열림)
WORKDIR /bis/source

# 컨테이너가 시작될 때 main.py 실행
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# ec2에서 돌아가는 이미지의 목적 : 코드 수정은 안할거고, run 만 하는거니까, 이미지 빌드하고 run 할 때 필요한 파일만 이미지에 넣으면 되겠음.
# requirements.txt, py로 끝나는 코드, .env도 필요