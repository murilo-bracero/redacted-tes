create-venv:
	python3 -m venv .venv

migrate:
#	alembic revision --autogenerate -m "my message"
	alembic upgrade head

install:
	pip install 

run-dev:
# 	change port if needed
	fastapi dev app/main.py --port 8080