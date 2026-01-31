FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_PROJECT_ENVIRONMENT=/usr/local

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock .
RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["./entrypoint.prod.sh"]

