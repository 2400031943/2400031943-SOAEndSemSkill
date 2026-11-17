FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed and python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]

