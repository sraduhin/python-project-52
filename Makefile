dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	python3 manage.py migrate
	poetry run gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

test: migrate
	poetry run python manage.py test tests/

console:
	poetry run python manage.py shell_plus --ipython
