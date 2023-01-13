FROM python:3.10.4-alpine

WORKDIR /opt/reporter

COPY ./requirements.txt /opt/reporter/requirements.txt

RUN apk add --no-cache gcc build-base musl-dev libffi-dev g++

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /opt/reporter/requirements.txt

RUN apk del gcc build-base musl-dev libffi-dev g++

COPY . /opt/reporter

ENV PYTHONPATH=/opt/reporter
