FROM python:3.9.6

ENV PYTHONBUFFERED=1

WORKDIR /application

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential curl nano

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install setuptools==75.8.0

RUN python3 -m pip install gunicorn==23.0.0

RUN python3 -m pip install -r requirements.txt

COPY . .
