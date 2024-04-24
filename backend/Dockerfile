FROM python:3.10.14-alpine3.19

WORKDIR /backend

COPY ./backend/requirements.txt .

RUN pip install -r requirements.txt

COPY . .