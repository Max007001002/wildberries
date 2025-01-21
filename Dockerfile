FROM python:3.11-slim

# Создадим рабочую директорию
WORKDIR /app

# Скопируем файл с зависимостями
COPY requirements.txt requirements.txt

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем всё остальное
COPY . .

# При запуске контейнера будем поднимать uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
