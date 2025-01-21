# Wildberries Service

**FastAPI + Aiogram (Webhook) + PostgreSQL + APScheduler для работы с продуктами Wildberries.**

## Описание

Проект предоставляет API для взаимодействия с данными о товарах с Wildberries. Основные функции:
- Получение данных по артикулу товара из API Wildberries.
- Сохранение данных в базу данных PostgreSQL.
- Создание и обновление товаров в базе данных через API.
- Запуск периодической задачи для сбора данных по артикулу каждые 30 минут.

## Требования

- Python >= 3.11
- Docker и Docker Compose
- PostgreSQL

## Установка и запуск

1. **Клонируйте репозиторий**

   ```bash
   git clone https://github.com/yourusername/wildberries_service.git
   cd wildberries_service

2. **Создайте и активируйте виртуальное окружение**

    ```python -m venv .venv
    source .venv/bin/activate  # Для Linux / macOS
    .venv\Scripts\activate  # Для Windows```

3. **Установите зависимости**

    ```pip install -r requirements.txt```

4. **Настройте переменные окружения**

    ```
    BOT_TOKEN=your_bot_token
    BEARER_TOKEN=your_bearer_token
    DATABASE_USER=postgres
    DATABASE_PASSWORD=postgres
    DATABASE_HOST=postgres_db
    DATABASE_PORT=5432
    DATABASE_NAME=wb_products_db
    WEBHOOK_DOMAIN=https://your_webhook_domain
    WEBHOOK_PATH=/webhook/bot
   ```

5. **Запуск Docker контейнеров**

    ```docker-compose up --build```

6. **Миграции базы данных**

    ```
    docker exec -it wb_service bash
    alembic upgrade head
   ```

7. **Использование API**

    ```
    Swagger UI: Для тестирования API перейдите по адресу http://localhost:8000/docs.
    Postman: Вы можете отправлять запросы через Postman, используя тот же URL и авторизационный токен, указанный в .env файле.
   ```
# Структура проекта
```
app/: Основной код приложения.
bot/: Логика взаимодействия с ботом через Aiogram.
api/: Эндпоинты API для работы с продуктами.
database/: Работа с базой данных (создание сессий, модели данных).
crud/: CRUD операции для работы с товарами.
schemas/: Схемы для запросов и ответов API.
scheduler/: Задачи для периодического сбора данных о товарах.
Dockerfile: Конфигурация для сборки Docker образа.
docker-compose.yml: Настройки для запуска Docker контейнеров.
```
# Примечания
Если у вас возникли проблемы с запуском контейнеров, убедитесь, что Docker и Docker Compose установлены и работают правильно.
Для успешной работы с API Wildberries необходимо иметь правильный BEARER_TOKEN, который используется для авторизации.
В случае возникновения ошибок с базой данных, проверяйте правильность подключения в файле .env.