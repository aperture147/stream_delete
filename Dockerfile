FROM python:3.8-alpine

LABEL maintainer="HaiVQ <me@haivq.com>"

ENV TZ="Asia/Ho_Chi_Minh"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY db_helper.py db_helper.py
COPY main.py main.py

ENTRYPOINT python main.py