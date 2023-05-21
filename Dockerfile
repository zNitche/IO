from python:3.10-slim

COPY . /io_app
WORKDIR /io_app

RUN apt update && apt -y install nano curl

RUN curl -o /io_app/io_app/static/libs/chart.js  https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.umd.min.js
RUN curl -o /io_app/io_app/static/libs/bootstrap.min.css  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css
RUN curl -o /io_app/io_app/static/libs/bootstrap.bundle.min.js  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js

RUN pip3 install -r requirements.txt

RUN chmod +x scripts/entrypoint.sh
RUN chmod +x scripts/celery_beat_entrypoint.sh
RUN chmod +x scripts/celery_entrypoint.sh