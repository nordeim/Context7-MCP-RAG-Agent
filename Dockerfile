# =============================================================================
# CONTEXT7 TERMINAL AI - PRODUCTION DOCKERFILE
# Multi-stage build for optimal security and size
# =============================================================================

# 🐍 Stage 1: Python Build Environment
FROM python:3.11-slim as builder

# Set build arguments
ARG POETRY_VERSION=1.7.1
ARG TARGETPLATFORM
ARG BUILDPLATFORM

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 🐍 Stage 2: Runtime Environment
FROM python:3.11-slim as runtime

# Set metadata
LABEL maintainer="Context7 Team"
LABEL version="1.0.0"
LABEL description="Context7 Terminal AI Agent"

# Create non-root user for security
RUN groupadd -r context7 && useradd -r -g context7 context7

# Install Node.js for MCP server
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Context7 MCP globally
RUN npm install -g @upstash/context7-mcp@latest

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY .env.example ./.env.example
COPY requirements.txt ./

# Create necessary directories
RUN mkdir -p /app/data /app/logs /home/context7/.context7 && \
    chown -R context7:context7 /app /home/context7

# Switch to non-root user
USER context7

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV CONTEXT7_LOG_FILE=/app/logs/context7.log
ENV CONTEXT7_HISTORY_PATH=/app/data/history.json
ENV CONTEXT7_MCP_CONFIG_PATH=/app/data/mcp.json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '/app'); from src.agent import Context7Agent; import asyncio; asyncio.run(Context7Agent().initialize())" || exit 1

# Expose port for potential web interface
EXPOSE 8080

# Default command
CMD ["python", "-m", "src.cli"]
