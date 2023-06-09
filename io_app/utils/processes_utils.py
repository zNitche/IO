from io_app.apps.core.tasks import ArchiveExtraction, DirectoryCompression, VideoCompatibilityConversion


def start_file_process_for_user(user_id, process_name, file_uuid, context=None):
    tasks = [ArchiveExtraction, DirectoryCompression, VideoCompatibilityConversion]

    for task in tasks:
        if task.__name__ == process_name:
            task.apply_async((user_id, file_uuid, context))
            break
