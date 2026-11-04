# Multi-stage production container for KAVACH AI Platform on Railway / Cloud Run
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY kavach_platform/01_KAVACH_Platform/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy source code and platform assets
COPY . /app

# Ensure runtime directories exist
RUN mkdir -p /app/kavach_platform/01_KAVACH_Platform/backend/data /app/kavach_platform/01_KAVACH_Platform/backend/qdrant_storage

# Environment variables ($PORT injected dynamically by Railway)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:/app/kavach_platform/01_KAVACH_Platform/backend:/app/kavach_platform/02_Bharat_Core_Banking:/app/kavach_platform/02_Banking_and_Results_Dashboard/implementation_banks"
ENV PORT=8000
EXPOSE 8000

# Container liveness check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Launch uvicorn web service
CMD ["sh", "-c", "uvicorn app.main:app --app-dir kavach_platform/01_KAVACH_Platform/backend --host 0.0.0.0 --port ${PORT}"]
