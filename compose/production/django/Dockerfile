# FROM docker.io/node:20-bookworm-slim as client-builder

# ARG APP_HOME=/app
# WORKDIR ${APP_HOME}

# COPY ./package.json ${APP_HOME}
# RUN npm install && npm cache clean --force
# COPY . ${APP_HOME}
# # ARG DJANGO_AWS_STORAGE_BUCKET_NAME
# # ENV DJANGO_AWS_STORAGE_BUCKET_NAME=${DJANGO_AWS_STORAGE_BUCKET_NAME}
# # ARG DJANGO_AWS_S3_CUSTOM_DOMAIN
# # ENV DJANGO_AWS_S3_CUSTOM_DOMAIN=${DJANGO_AWS_S3_CUSTOM_DOMAIN}
# RUN npm run build --omit=dev
# define an alias for the specific python version used in this file.
FROM docker.io/python:3.12.4-slim-bookworm AS python
# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update ; apt-get dist-upgrade -y ; apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg dependencies
  libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/home/bot/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

RUN useradd --user-group --create-home --shell /bin/bash bot

WORKDIR ${APP_HOME}

# RUN addgroup --system django \
#   && adduser --system --ingroup django django

ENV HOME=${APP_HOME}
# Install required system dependencies
RUN apt-get update ; apt-get dist-upgrade -y ; apt-get install --no-install-recommends -y \
  # psycopg dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN python -m venv /home/bot/venv

ENV PATH="/home/bot/venv/bin:$PATH"
# use wheels to install python dependencies
RUN python -m pip install -U pip --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/


COPY --chown=bot:bot ./compose/production/django/entrypoint /home/bot/entrypoint
RUN sed -i 's/\r$//g' /home/bot/entrypoint
RUN chmod +x /home/bot/entrypoint


COPY --chown=bot:bot ./compose/production/django/start /home/bot/start
RUN sed -i 's/\r$//g' /home/bot/start
RUN chmod +x /home/bot/start
COPY --chown=bot:bot ./compose/production/django/celery/worker/start /home/bot/start-celeryworker
RUN sed -i 's/\r$//g' /home/bot/start-celeryworker
RUN chmod +x /home/bot/start-celeryworker


COPY --chown=bot:bot ./compose/production/django/celery/beat/start /home/bot/start-celerybeat
RUN sed -i 's/\r$//g' /home/bot/start-celerybeat
RUN chmod +x /home/bot/start-celerybeat


COPY --chown=bot:bot ./compose/production/django/celery/flower/start /home/bot/start-flower
RUN sed -i 's/\r$//g' /home/bot/start-flower
RUN chmod +x /home/bot/start-flower

COPY --chown=bot:bot ./compose/production/django/gunicorn-cfg.py /home/bot/gunicorn-cfg.py

# copy application code to WORKDIR
# COPY --from=client-builder --chown=bot:bot ${APP_HOME} ${APP_HOME}

RUN    mkdir -p $HOME/staticfiles
RUN   chown -R bot:bot $HOME/staticfiles


COPY --chown=bot:bot . $HOME

# make django owner of the WORKDIR directory as well.
RUN chown -R bot:bot $HOME


USER bot

RUN DATABASE_URL="" \
  CELERY_BROKER_URL="" \
  DJANGO_SETTINGS_MODULE="config.settings.test" \
  python manage.py makemessages -a -e html,txt,py

RUN DATABASE_URL="" \
  CELERY_BROKER_URL="" \
  DJANGO_SETTINGS_MODULE="config.settings.test" \
  python manage.py compilemessages

# RUN DATABASE_URL="" \
#   CELERY_BROKER_URL="" \
#   DJANGO_SETTINGS_MODULE="config.settings.test" \
#   python manage.py collectstatic --noinput --clear

ENTRYPOINT ["/home/bot/entrypoint"]
