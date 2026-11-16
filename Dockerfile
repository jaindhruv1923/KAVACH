# Production container for KAVACH Unified Autonomous AI Defense Ecosystem
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (curl for health check, git for AST analysis)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy complete project
COPY . /app

# Create clean Linux symlink so directory path with spaces & ampersand is accessible cleanly
RUN ln -s "/app/PRJ-IV &AgenticAi Final Work" /app/kavach_core

# Ensure persistent directories exist
RUN mkdir -p "/app/PRJ-IV &AgenticAi Final Work/kavach_platform/01_KAVACH_Platform/backend/data" \
    "/app/PRJ-IV &AgenticAi Final Work/bharat_core_banking/data" \
    "/app/PRJ-IV &AgenticAi Final Work/kavach_platform/02_Banking_and_Results_Dashboard/results_dashboard/data"

# Environment configuration
ENV PYTHONUNBUFFERED=1
ENV KAVACH_OFFLINE=1
ENV PYTHONPATH="/app:/app/kavach_core:/app/kavach_core/kavach_platform/01_KAVACH_Platform/backend"
ENV PORT=8000
EXPOSE 8000

# Railway liveness health check
HEALTHCHECK --interval=20s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Launch uvicorn web service binding to 0.0.0.0 and dynamic $PORT injected by Railway
CMD ["sh", "-c", "uvicorn app.main:app --app-dir '/app/kavach_core/kavach_platform/01_KAVACH_Platform/backend' --host 0.0.0.0 --port ${PORT}"]
