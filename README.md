# Question and answer API (FastAPI + SQLAlchemy + Alembic + Pydantic + Docker + Pytest)

Минимальный CRUD-сервис управления вопросами и ответами. 

Методы API:
Вопросы (Questions):
GET /questions/ — список всех вопросов
POST /questions/ — создать новый вопрос
GET /questions/{id} — получить вопрос и все ответы на него
DELETE /questions/{id} — удалить вопрос (вместе с ответами)


Ответы (Answers):
POST /questions/{id}/answers/ — добавить ответ к вопросу
GET /answers/{id} — получить конкретный ответ
DELETE /answers/{id} — удалить ответ


## Быстрый старт (Docker Compose)
```bash
docker compose up -d
docker compose exec api alembic upgrade head

http://localhost:8000/docs
```
## Запуск тестов 
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v -s
```

## Adminer (управление базой данных)
```bash
http://localhost:8080
```

## Alembic (миграция базы данных)
```bash
alembic revision --autogenerate -m "(название)"
alembic upgrade head
```
