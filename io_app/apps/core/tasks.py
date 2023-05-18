from io_app.celery import app
from io_app.apps.core.task.archive_extraction import ArchiveExtraction


ArchiveExtraction = app.register_task(ArchiveExtraction())
