FROM python:3.12-slim

WORKDIR /app

# Copy requirements from root
COPY requirements.txt .

# Copy the auth service code
COPY ./ml_microservices/train/ .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5003

# CRITICAL: Add --host 0.0.0.0
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5003"]