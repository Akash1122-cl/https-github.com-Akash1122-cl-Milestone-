FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY apps/api/ .

EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
