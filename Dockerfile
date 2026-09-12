# Базовый образ с Python
FROM python:3.12-slim

# Переменные окружения Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Системные зависимости (нужны для psycopg2 и Pillow)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска через Daphne (ASGI, поддерживает WebSockets)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "questboard.asgi:application"]