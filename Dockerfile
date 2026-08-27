FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://python-poetry.org | python3 -

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-interaction --no-ansi 

COPY . .

EXPOSE 8000

CMD ["sh", "-c", \
    "alembic -c backend/alembic.ini upgrade head \
    && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]