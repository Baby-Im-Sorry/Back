# 베이스 이미지로 Python 이미지 사용
FROM python:3.9

# 로컬에 있는 파일을 이미지에 복사하기
COPY requirements.txt /bis/
COPY .env.production /bis/
COPY source /bis/source/

# 필요한 Python 패키지 설치 (pip freeze > requirements.txt 명령을 통해 requirements.txt를 갱신해주는 작업이 선수로 필요)
RUN pip install -r /bis/requirements.txt
RUN apt-get update && apt-get install -y cron && apt-get install -y vim
RUN chmod +x /entrypoint.sh

# 컨테이너의 작업 디렉터리 설정 (쉘이 초기에 bis 폴더에서 열림)
WORKDIR /bis/source

# 컨테이너가 시작될 때 main.py 실행
CMD ["/bis/source/shell/entrypoint.sh"]


