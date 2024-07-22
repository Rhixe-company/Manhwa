from time import sleep
from celery.utils.log import get_task_logger
from celery_progress.backend import ProgressRecorder
from django.core.management import call_command
from celery.schedules import crontab
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from config.celery_app import app

logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        call_command("crawl")
    )




@shared_task(bind=True)
def my_task(self, duration):

    call_command("crawl")
    logger.info("Done   Downloading")
    progress_recorder = ProgressRecorder(self)
    for i in range(10):
        sleep(duration)
        progress_recorder.set_progress(i + 1, 10, f"On iteration {i+1}")

    return "Done   Downloading"
