import zipfile
import os
import shutil
import tempfile
from django.conf import settings
from io_app.celery_tasks.user_task_base import UserTaskBase
from io_app.apps.storage_manager import models
from io_app.consts import ProcessesConsts
from io_app.utils import files_utils


class ArchiveExtraction(UserTaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 10800

        self.file_uuid = ""

    def run(self, owner_id, file_uuid):
        self.owner_id = owner_id
        self.file_uuid = file_uuid

        self.process_cache_key = f"{self.owner_id}_{self.get_process_name()}_{self.timestamp}"

        self.mainloop()

    def calc_progres(self, current_step, max_steps):
        self.task_progress = int(current_step * 100 / max_steps)

    def update_progress_callback(self, current_step, total_steps):
        self.calc_progres(current_step, total_steps)
        self.update_process_data()

    def get_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROGRESS: self.task_progress,
            ProcessesConsts.FILE_UUID: self.file_uuid,
        }

        return process_data

    def extract_zip(self, archive_path, output_path):
        with zipfile.ZipFile(archive_path, "r") as zip_file:
            archive_files_count = len(zip_file.infolist())

            for file_id, member in enumerate(zip_file.infolist()):
                try:
                    zip_file.extract(member, output_path)

                except zipfile.error as e:
                    pass

                self.update_progress_callback(file_id + 1, archive_files_count)

    def add_files(self, files_path, output_path):
        new_dir_model = models.Directory(owner_id=self.owner_id, name=self.timestamp)
        new_dir_model.save()

        for file in os.listdir(output_path):
            file_path = os.path.join(output_path, file)

            file_model = models.File(owner_id=self.owner_id,
                                     name=file,
                                     extension=file.split(".")[-1],
                                     directory=new_dir_model,
                                     size=files_utils.get_size_of_file(file_path),
                                     uuid=files_utils.generate_uuid())
            file_model.save()

            shutil.move(file_path, os.path.join(files_path, file_model.uuid))

            new_dir_model.files.add(file_model)
            new_dir_model.save()

    def mainloop(self):
        self.update_process_data()

        try:
            files_path = os.path.join(settings.STORAGE_PATH, str(self.owner_id))
            archive_path = os.path.join(files_path, self.file_uuid)

            with tempfile.TemporaryDirectory() as tmp_dir_name:
                output_path = os.path.join(tempfile.gettempdir(), tmp_dir_name)

                self.extract_zip(archive_path, output_path)
                self.add_files(files_path, output_path)

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
