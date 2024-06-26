# syntax=docker/dockerfile:1
FROM python:3.12.3-alpine

RUN apk add --no-cache curl

WORKDIR /app
COPY pyproject.toml /app/
COPY awesome_app /app/awesome_app

RUN pip install --no-cache-dir -e .

ENV PYTHONPATH=/app

ENV FLASK_RUN_PORT=8000
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP="awesome_app/app.py"

ENTRYPOINT ["flask", "run"]