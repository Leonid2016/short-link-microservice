FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY links-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY links-service/app ./app
COPY shared ./shared
EXPOSE 5002
CMD ["python", "-m", "app"]
