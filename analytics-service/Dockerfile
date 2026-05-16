FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY analytics-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY analytics-service/app ./app
EXPOSE 5003
CMD ["python", "-m", "app"]
