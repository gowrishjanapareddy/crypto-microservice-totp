###############################
# Stage 1: Builder
###############################
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system deps for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --default-timeout=200 --retries 10 --no-cache-dir -r requirements.txt



###############################
# Stage 2: Runtime
###############################
FROM python:3.11-slim

ENV TZ=UTC

# Install cron + timezone
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Set timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

WORKDIR /app

# Copy installed Python dependencies
COPY --from=builder /usr/local /usr/local

# Copy entire application
COPY . .

# Copy cron file
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy start script
COPY start.sh /start.sh

# Copy scripts (ensure correct path)
COPY scripts/ /app/scripts/


###############################
# Permissions
###############################

RUN chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron && \
    chmod +x /app/scripts/log_2fa_cron.py && \
    chmod +x /start.sh


###############################
# Data directories
###############################
RUN mkdir -p /data && chmod 755 /data
RUN mkdir -p /cron && chmod 755 /cron


###############################
# Start cron + API
###############################
CMD ["/bin/sh", "/start.sh"]

EXPOSE 8080
