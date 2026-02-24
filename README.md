# SMC Project - Система генерации учебных документов

Монорепозиторий для системы генерации рабочих программ, аннотаций и фондов оценочных средств.

## Структура проекта

- **`SMC-package/`** - Общий пакет с бизнес-логикой и моделями данных
- **`API-lib/`** - Клиентская библиотека для взаимодействия с сервисом
- **`service/`** - FastAPI сервис, реализующий HTTP API

## Требования

- Python 3.11+
- Poetry или pip
- Docker (опционально)

## Быстрый старт

```bash
# Клонировать репозиторий
git clone <url>

# Установить все зависимости
cd SMC-package && pip install -e .
cd ../API-lib && pip install -e .
cd ../service && pip install -r requirements.txt

# Запустить сервис
cd service && uvicorn src.main:app --reload