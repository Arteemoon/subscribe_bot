FROM python:3.9-buster

WORKDIR /opt/app


COPY . /opt/app/


RUN pip install --upgrade pip && pip install -r requirements.txt
