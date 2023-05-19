from io_app.celery import app
from io_app.apps.storage_manager.task.archive_extraction import ArchiveExtraction
from io_app.apps.storage_manager.task.files_cleaner import FilesCleanerProcess


ArchiveExtraction = app.register_task(ArchiveExtraction())
FilesCleanerProcess = app.register_task(FilesCleanerProcess())
