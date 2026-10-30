# Use an official lightweight Python runtime
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl (used for container healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition first (leverages Docker layer caching)
COPY requirements.txt .

# Install dependencies without cache to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files, model artifact, and startup script
COPY app/ ./app/
COPY start.sh .

# Make the startup script executable
RUN chmod +x start.sh

# Expose backend (8000) and frontend (8501) ports
EXPOSE 8000
EXPOSE 8501

# Run both services via start.sh
CMD ["./start.sh"]