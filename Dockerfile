FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY apps/api/ .

# Create __init__.py files to make modules importable
RUN touch /app/__init__.py
RUN touch /app/core/__init__.py
RUN touch /app/routers/__init__.py

EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
