FROM python:3.12-slim
RUN sudo apt update -y && sudo apt install awscli -y
WORKDIR /app

# 1. Copy only the files needed for installation first
# This allows Docker to cache the installed packages layer
COPY requirements.txt .
COPY setup.py .  
COPY ./src /app/src
# 2. Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 3. Now, copy the rest of your application source code
ENV PYTHONPATH=/app/src
COPY . .

EXPOSE 3004

# This command assumes your uvicorn entrypoint is in the root of the project.
# You might need to adjust "app:app" if it's inside a subfolder, 
# e.g., "ml_microservices.auth.app:app"
CMD ["uvicorn", "ml_microservices.train.app:app", "--host", "0.0.0.0", "--port", "3004"]
