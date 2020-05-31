FROM python:3.8-alpine

ENV UNBUFFERED 1

COPY ./requirements.txt /requirements

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user