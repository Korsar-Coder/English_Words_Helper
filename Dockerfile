FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-interaction --no-ansi 

COPY . .

EXPOSE 8000

CMD ["sh", "-c", \
    "alembic -c backend/alembic.ini upgrade head \
    && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]