FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка конкретной версии Poetry
RUN pip install poetry==1.8.0

# Копируем все пакеты
COPY SMC-package /SMC-package
COPY API-lib /API-lib
COPY service /service

# Устанавливаем SMC-package (удаляем lock файл)
WORKDIR /SMC-package
RUN rm -f poetry.lock && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Устанавливаем API-lib (удаляем lock файл)
WORKDIR /API-lib
RUN rm -f poetry.lock && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Устанавливаем сервис
WORKDIR /service
RUN rm -f poetry.lock && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Создаем необходимые директории
RUN mkdir -p /service/uploads /service/generated

# Устанавливаем PYTHONPATH
ENV PYTHONPATH="/SMC-package/src:/API-lib/src:/service/src"

WORKDIR /service

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]