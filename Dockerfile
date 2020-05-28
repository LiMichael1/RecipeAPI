FROM python:3.8-alpine
MAINTAINER Michael Li

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update
# package manager add update package , Permanent
RUN apk add --update --no-cache postgresql-client jpeg-dev
# temp build dependencies while installing requirements
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip3 install -r /requirements.txt

# delete temp build dependencies
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# images go in media directory
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
# owner can do anything with this directory
RUN chmod -R 755 /vol/web
USER user

