FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо вміст папки backend у робочу папку /app
COPY backend/ .

EXPOSE 8000

# Запускаємо uvicorn з модулем app (app.py у /app)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

