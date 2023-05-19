from django.conf import settings
from io_app.celery_tasks.background_task_base import BackgroundTaskBase
from io_app.consts import TasksDelays
from io_app.utils import files_utils
from io_app.apps.storage_manager import models
import time
import os


class FilesCleanerProcess(BackgroundTaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 60

        self.storage_path = settings.STORAGE_PATH

    def run(self):
        if not self.check_if_same_task_running():
            self.process_cache_key = f"{self.get_process_name()}_{self.timestamp}"
            self.mainloop()

        else:
            self.logger.info(f"[{self.get_process_name()}] - skipped, already running")

    def collect_files_sizes(self, files_in_db):
        files_sizes_struct = {}

        for user_id in os.listdir(self.storage_path):
            user_files_path = os.path.join(self.storage_path, user_id)

            if os.path.isdir(user_files_path):
                for file_uuid in os.listdir(user_files_path):
                    if file_uuid not in files_in_db:
                        file_path = os.path.join(user_files_path, file_uuid)

                        files_sizes_struct[file_uuid] = {
                            "path": file_path,
                            "size": files_utils.get_size_of_file(file_path)
                        }

        return files_sizes_struct

    def get_files_to_be_removed(self, old_files_sizes_struct, current_files_sizes_struct):
        files_to_be_removed = {}

        for file_uuid in current_files_sizes_struct.keys():
            if file_uuid in old_files_sizes_struct.keys():
                old_file_size = old_files_sizes_struct[file_uuid]["size"]
                current_file_size = current_files_sizes_struct[file_uuid]["size"]

                if old_file_size == current_file_size:
                    files_to_be_removed[file_uuid] = current_files_sizes_struct[file_uuid]

        return files_to_be_removed

    def clean_files(self, files_struct):
        for file_uuid in files_struct.keys():
            file_path = files_struct[file_uuid]["path"]

            if os.path.exists(file_path):
                os.remove(file_path)

                self.logger.info(f"[{self.get_process_name()}] - removed file '{file_path}'")

    def mainloop(self):
        try:
            self.update_process_data()
            files_uuids = [file.uuid for file in models.File.objects.all()]

            files_sizes_struct = self.collect_files_sizes(files_uuids)
            time.sleep(TasksDelays.FILES_CLEANER_WAIT)

            current_files_sizes_struct = self.collect_files_sizes(files_uuids)
            files_to_be_removed = self.get_files_to_be_removed(files_sizes_struct, current_files_sizes_struct)

            self.clean_files(files_to_be_removed)

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
