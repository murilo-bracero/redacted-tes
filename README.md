# redacted-tes

## Configuration

A aplicação depende das seguintes variáveis de ambiente para ser executada:

- DB_USER :: nome de usuário do banco de dados
- DB_PASSWORD :: senha de usuário do banco de dados
- DB_HOST :: host do banco de dados e.g. localhost
- DB_PORT :: porta de rede do banco de dados e.g. 5432
- DB_NAME :: nome do banco de dados, e.g. postgres

## Migrations

Esta aplicação utiliza o pacote alambic para realizar as migrações do banco de dados, para utilizá-lo, instale a dependência:

```sh
pip install alembic
```

Crie uma nova migration (opcional):

```sh
alembic revision --autogenerate -m "bootstrap database"
```

Em seguida, execute-a contra o banco de dados:

```sh
alembic upgrade head
```

**DISCLAIMER**: As variáveis de ambiente listadas anteriormente são necessárias para este processo

## Executando

### Localmente

#### Requisitos

- Variáveis de ambiente populadas
- Banco PostgreSQL versão 14 ou superior
- Python versão 3.10 ou superior 

#### Passo a passo

Cre um novo ambiente virtual e ative-o (opcional):

```sh
make create-venv
source ./.venv/bin/activate
```

Instale as dependências da aplicação, de preferência em um venv:

```sh
pip install --no-cache-dir .
```

ou, utilizando o makefile

```sh
make install
```

Para executar a aplicação localmente para desenvolvimento, utilize o comando:

```sh
python -m fastapi dev app/main.py --port 8080
```

ou:

```sh
make run-dev
```

Para executar a aplicação em modo definitivo, o mais próximo de produção possível, use este comando:

```sh
python -m fastapi run app/main.py --port 8080
```

### Utilizando Docker/Docker compose (recomendado)

Execute a suite completa da aplicação utilizando o arquivo docker-compose.yaml na pasta deployments:

```sh
docker compose -f deployments/docker-compose.yaml up -d --build
```

Este comando fará o deploy:

- Do banco de dados PostgreSQL
- De um container para realizar as migrations
- Da aplicação Python
