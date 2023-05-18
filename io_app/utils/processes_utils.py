from io_app.apps.core.tasks import ArchiveExtraction
from io_app.consts import ProcessesConsts


def start_file_process_for_user(user_id, process_name, file_uuid):
    tasks = [ArchiveExtraction]
    process_name = get_process_for_file_internal_name(process_name)

    for task in tasks:
        if task.__name__ == process_name:
            task.apply_async((user_id, file_uuid))
            break


def get_process_for_file_internal_name(process_name):
    name = None

    for process_internal_name in ProcessesConsts.PROCESSES_FOR_FILES_NAMES.keys():
        if ProcessesConsts.PROCESSES_FOR_FILES_NAMES[process_internal_name] == process_name:
            name = process_internal_name
            break

    return name
