FROM python:3.11-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY QuickHub /QuickHub
WORKDIR /QuickHub
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

RUN mkdir -p /QuickHub/logs && chown service-user:service-user /QuickHub/logs

USER service-user
