FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /cron /data \
    && chmod 0644 cron/2fa-cron \
    && crontab cron/2fa-cron

EXPOSE 8080

CMD ["sh", "-c", "cron && uvicorn app:app --host 0.0.0.0 --port 8080"]
