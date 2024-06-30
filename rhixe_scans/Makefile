PYTHON = ../venv/Scripts/python

makemessages:
	$(PYTHON) ./manage.py makemessages -a -e html,txt,py 

compilemessages:
	$(PYTHON) ./manage.py compilemessages

start:
	$(PYTHON) ./manage.py runserver

migrations:
	$(PYTHON) ./manage.py makemigrations

migrate:
	$(PYTHON) ./manage.py migrate

migrate-social:
	$(PYTHON) ./manage.py migrate socialaccount

superuser:
	$(PYTHON) ./manage.py createsuperuser

static:
	$(PYTHON) ./manage.py collectstatic 

crawl:
	$(PYTHON) ./manage.py crawl

test:
	$(PYTHON) ./manage.py test

shell:
	$(PYTHON) ./manage.py shell_plus

celery-beat:
	$(PYTHON)  celery -A config.celery_app beat -l info

celery-worker:
	$(PYTHON)  -m celery -A config.celery_app worker -Q normal -l info


dev:
	npm run dev

build:
	npm run build

clean:
	npm run clean