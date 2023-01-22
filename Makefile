dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	python3 manage.py migrate
	poetry run gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager --exclude=migrations

tests:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run ./manage.py test
	poetry run coverage report --include=*/models.py,*/views.py,*/urls.py,*/utils.py,*/filters.py
	poetry run coverage xml --include=*/models.py,*/views.py,*/urls.py,*/utils.py,*/filters.py

console:
	poetry run python manage.py shell_plus --ipython
