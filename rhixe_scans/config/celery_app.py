from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    worker_max_tasks_per_child=1,
    broker_pool_limit=None,
    result_backend="django-db",
    include=[
        "scraper.tasks",
    ],
)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
