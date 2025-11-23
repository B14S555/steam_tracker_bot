FROM python:3.11-slim

# рабочая директория в контейнере
WORKDIR /app

# копируем файлы проекта
COPY . /app

# установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# команда запуска
CMD ["python", "main.py"]
