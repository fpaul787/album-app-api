FROM python:3.7-alpine
LABEL MAINTAINER="Frantz"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# install postgresql client
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user

#change owner of /vol directory
RUN chown -R user: user /vol

# change permissions
RUN chown -R user:user /vol/web
USER user