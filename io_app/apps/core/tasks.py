from io_app.celery import app
from io_app.apps.storage_manager.task.archive_extraction import ArchiveExtraction
from io_app.apps.storage_manager.task.files_cleaner import FilesCleanerProcess
from io_app.apps.storage_manager.task.directory_compression import DirectoryCompression


ArchiveExtraction = app.register_task(ArchiveExtraction())
DirectoryCompression = app.register_task(DirectoryCompression())

FilesCleanerProcess = app.register_task(FilesCleanerProcess())
