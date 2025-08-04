# Builder stage
FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app

# Install UV
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src ./src

# Create virtual environment and install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv sync

# Runtime stage
FROM python:3.11-slim-bookworm

RUN apt-get update && \
    apt-get install -y libpq5 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
WORKDIR /app

# Copy virtual environment and source code
COPY --from=builder /app/.venv .venv
COPY --from=builder /app/src ./src

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Run the application - note the "src." prefix
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio"]
