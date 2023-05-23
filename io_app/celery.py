import os
from celery import Celery
from celery.signals import worker_ready
from io_app.consts import TasksDelays


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "io_app.settings")

app = Celery("io_app")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    app.conf.beat_schedule["FilesCleanerProcess"] = {
        "task": "io_app.apps.storage_manager.task.files_cleaner.FilesCleanerProcess",
        "schedule": TasksDelays.FILES_CLEANER_PROCESS_INTERVAL,
    }


@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
         sender.app.send_task("io_app.apps.storage_manager.task.files_cleaner.FilesCleanerProcess", connection=conn)
         sender.app.send_task("io_app.apps.storage_manager.task.tmp_cleaner.TmpCleanerProcess", connection=conn)
