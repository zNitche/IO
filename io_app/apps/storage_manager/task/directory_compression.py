import os
import shutil
import tempfile
from django.conf import settings
from io_app.celery_tasks.user_task_base import UserTaskBase
from io_app.apps.storage_manager import models
from io_app.consts import ProcessesConsts
from io_app.utils import files_utils


class DirectoryCompression(UserTaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 60

        self.directory_uuid = ""

    def run(self, owner_id, file_uuid):
        self.owner_id = owner_id
        self.directory_uuid = file_uuid

        self.process_cache_key = f"{self.owner_id}_{self.get_process_name()}_{self.timestamp}"

        self.mainloop()

    def calc_progres(self, current_step, max_steps):
        self.task_progress = int(current_step * 100 / max_steps)

    def get_work_update_callback(self, current_step, total_steps):
        self.calc_progres(current_step, total_steps)
        self.update_process_data()

    def get_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROGRESS: self.task_progress,
            ProcessesConsts.FILE_UUID: self.directory_uuid,
        }

        return process_data

    def get_directory_files_data_struct(self, directory_files, files_path):
        files_data_struct = {}

        for file in directory_files:
            files_data_struct[file.uuid] = {
                "name": file.name,
                "path": os.path.join(files_path, file.uuid)
            }

        return files_data_struct


    def mainloop(self):
        self.update_process_data()

        try:
            files_path = os.path.join(settings.STORAGE_PATH, str(self.owner_id))
            directory = models.Directory.objects.filter(owner_id=self.owner_id, uuid=self.directory_uuid).first()

            files_data_struct = self.get_directory_files_data_struct(directory.files.all(), files_path)

            archive_name = f"{self.directory_uuid}.zip"

            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_dir_path = os.path.join(tempfile.gettempdir(), tmpdir)
                archive_path = os.path.join(tmp_dir_path, archive_name)

                files_utils.zip_files(archive_path, files_data_struct, progress_callback=self.calc_progres)

                archive_uuid = files_utils.generate_uuid()
                archive_final_path = os.path.join(files_path, archive_uuid)

                shutil.move(archive_path, archive_final_path)

            archive_file = models.File(owner_id=self.owner_id,
                                       name=archive_name,
                                       extension="zip",
                                       size=files_utils.get_size_of_file(archive_final_path),
                                       uuid=archive_uuid)

            archive_file.save()

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
