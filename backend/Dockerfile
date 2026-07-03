FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치
RUN playwright install --with-deps chromium

COPY . .

# API: uvicorn app.main:app
# Worker: python run_worker.py