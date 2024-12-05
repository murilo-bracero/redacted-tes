FROM python:3.13.1-alpine

RUN addgroup -S apprunnergroup && adduser -S apprunneruser -G apprunnergroup

USER apprunneruser

WORKDIR /code

COPY ./pyproject.toml ./pyproject.toml

# --upgrade tag is optional since cache is already disabled
RUN pip install --no-cache-dir .

COPY ./app ./app

EXPOSE 80

ENV ENV=prd

CMD ["python", "-m", "fastapi", "run", "app/main.py", "--port", "80"]