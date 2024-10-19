# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /project
RUN pip list
COPY requirements-dev-testing.txt requirements.txt
RUN pip install -r requirements.txt
