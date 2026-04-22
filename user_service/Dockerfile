# Використовуємо легкий образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файл залежностей
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код сервісу
COPY . .

# Команда для запуску
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]