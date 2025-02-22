FROM python:3.9.6

ENV PYTHONBUFFERED=1

WORKDIR /scrapy_tools

RUN apt-get update && apt-get install -y cron nano && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

COPY . .

COPY crontab /etc/cron.d/scrapy-cron

RUN chmod 0644 /etc/cron.d/scrapy-cron && crontab /etc/cron.d/scrapy-cron

RUN mkdir -p /var/log && touch /var/log/scrapy_vikings.log && touch /var/log/scrapy_norsemen.log && touch /var/log/scrapy_vikings_nfl.log

CMD ["sh", "-c", "cron -f"]
