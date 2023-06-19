from io_app.celery import app
from io_app.apps.storage_manager.task.archive_extraction import ArchiveExtraction
from io_app.apps.storage_manager.task.files_cleaner import FilesCleanerProcess
from io_app.apps.storage_manager.task.directory_compression import DirectoryCompression
from io_app.apps.storage_manager.task.tmp_cleaner import TmpCleanerProcess
from io_app.apps.storage_manager.task.video_compatibility_conversion import VideoCompatibilityConversion


ArchiveExtraction = app.register_task(ArchiveExtraction())
DirectoryCompression = app.register_task(DirectoryCompression())
VideoCompatibilityConversion = app.register_task(VideoCompatibilityConversion())

FilesCleanerProcess = app.register_task(FilesCleanerProcess())
TmpCleanerProcess = app.register_task(TmpCleanerProcess())
