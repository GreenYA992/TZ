# Order Management API

REST API для управления заказами, товарами и клиентами с использованием FastAPI и PostgreSQL.

## Зависимости

- **Python 3.11+**
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy 2.0** - ORM для работы с БД
- **PostgreSQL 17** - реляционная база данных
- **Docker** - контейнеризация приложения
- **Uvicorn** - ASGI-сервер

## Установка и запуск

### Локальная разработка (без Docker)

1. **Клонирование репозитория**
   ```bash
   git clone <your-repo-url>
   cd your-project
   ```
2. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```
3. **Настройка базы данных**
   - **Создайте .env файл, со строкой подключения к БД**
     **(Уже есть в проекте, не создавал .gitignore, так как БД локальная)**
   - **Создайте БД PostgreSQL**
     ```bash
     python run.py
     ```
   - **Создайте тестовых данных**
     ```bash
     python add_data.py
     ```
## Запуск с Docker
1. **Сборка и запуск контейнеров**
     ```bash
     docker-compose up --build
     ```
2. **Добавление тестовых данных**
     ```bash
     docker-compose exec app python add_data.py
     ```
## Приложение будет доступно по адресу:
   - **API: http://localhost:8000**
   - **Документация: http://localhost:8000/docs** 