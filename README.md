Аналитика доходности инвестиционного портфеля Тиньков
======================================================

# Переменные окружения
```
export TINKOFF_TOKEN=some_tinkoff_token
```
Поддерживается .env файл.

Здесь `TINKOFF_TOKEN` это токен Тиньков инвестиций.

# Использование
Для запуска проекта нужно активировать окружение, установить зависимости и запустить скрипт `go.py`.

## Poetry
```
poetry shell
poetry install 
python go.py
```

## PIP
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python go.py
```