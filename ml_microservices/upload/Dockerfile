FROM python:3.12-slim

WORKDIR /app

# Copy requirements from root
COPY requirements.txt .

# Copy the auth service code
COPY ./ml_microservices/upload/ .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5001

# CRITICAL: Add --host 0.0.0.0
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"]