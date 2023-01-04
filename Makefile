start:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

test: migrate
	poetry run python manage.py test tests/

console:
	poetry run python manage.py shell_plus --ipython
