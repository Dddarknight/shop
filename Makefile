lint:
	poetry run flake8

install:
	poetry install

run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate
