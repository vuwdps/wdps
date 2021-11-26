# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
ARG PATH
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY . .

RUN python3 starter_code.py $PATH
