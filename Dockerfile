# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables for clean logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Cloud Run injects PORT environment variable (default 8080)
ENV PORT=8080
EXPOSE 8080

# Start server using run.py
CMD ["python", "run.py"]
