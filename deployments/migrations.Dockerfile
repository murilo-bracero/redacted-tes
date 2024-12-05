FROM python:3.13.1-alpine

RUN addgroup -S apprunnergroup && adduser -S apprunneruser -G apprunnergroup

USER apprunneruser

WORKDIR /code

COPY ./pyproject.toml ./pyproject.toml

# --upgrade tag is optional since cache is already disabled
RUN pip install --no-cache-dir .

COPY ./app ./app

COPY ./migrations ./migrations

COPY ./alembic.ini ./alembic.ini

ENV ENV=prd

CMD ["python", "-m", "alembic", "upgrade", "head"]