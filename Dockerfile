FROM python:3.8-alpine
MAINTAINER Michael Li

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update
# package manager add update package , don't store in docker
RUN apk add --update --no-cache postgresql-client
# temp build dependencies while installing requirements
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip3 install -r /requirements.txt

# delete temp build dependencies
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
