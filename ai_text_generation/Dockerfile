FROM python:3.13-slim-bookworm AS base
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

FROM base AS builder

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

FROM base AS final

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application files
COPY . .

EXPOSE 5000

# Set environment variables for production
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]