#!/bin/sh

echo "Starting cron..."
cron

echo "Starting API..."
uvicorn app:app --host 0.0.0.0 --port 8080