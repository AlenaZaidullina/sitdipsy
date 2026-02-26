FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта в контейнер
COPY . .

# Создание папок для статики и медиа
RUN mkdir -p staticfiles media

# Сборка статики
RUN python manage.py collectstatic --noinput  --clear
# Проверка, что статика собралась корректно
RUN echo "Checking static files..." && \
    find  staticfiles -name "*.js" | grep testimonials && \
    echo "Static files collected successfully"

# Открывается порт для внешних подключений
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CBT_psy.wsgi:application"]
