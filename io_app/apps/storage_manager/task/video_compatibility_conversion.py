from django.conf import settings
from io_app.celery_tasks.user_task_base import UserTaskBase
from io_app.apps.storage_manager import models
from io_app.consts import ProcessesConsts
from io_app.utils import files_utils, media_utils
import subprocess
import os
import shutil
import re


class VideoCompatibilityConversion(UserTaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 10800

        self.file_uuid = ""
        self.frames_count = None
        self.re_encode = False

    def run(self, owner_id, file_uuid, context):
        self.owner_id = owner_id
        self.file_uuid = file_uuid

        if context:
            self.re_encode = context.get("re_encode")

        self.process_cache_key = f"{self.owner_id}_{self.get_process_name()}_{self.timestamp}"

        self.mainloop()

    def calc_progress(self, current_step, max_steps):
        self.task_progress = int(current_step * 100 / max_steps)

    def update_progress_callback(self, current_step, total_steps):
        self.calc_progress(current_step, total_steps)
        self.update_process_data()

    def get_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROGRESS: self.task_progress,
            ProcessesConsts.FILE_UUID: self.file_uuid,
            ProcessesConsts.RE_ENCODE: self.re_encode,
        }

        return process_data

    def get_current_processing_frame(self, stdout_row):
        frame_id = None

        if "frame=" in stdout_row:
            regex = re.compile("frame=(.*)fps=")
            result = regex.search(stdout_row)

            frame_id = int(result.group(1).strip())

        return frame_id

    def add_file(self, file_uuid, file_extension, file_path):
        files_path = os.path.join(settings.STORAGE_PATH, str(self.owner_id))
        final_file_path = os.path.join(files_path, file_uuid)

        shutil.move(file_path, final_file_path)

        file_model = models.File(owner_id=self.owner_id,
                                 name=file_uuid,
                                 extension=file_extension,
                                 size=files_utils.get_size_of_file(final_file_path),
                                 uuid=file_uuid)
        file_model.save()

    def mainloop(self):
        self.update_process_data()

        try:
            file = models.File.objects.filter(owner_id=self.owner_id, uuid=self.file_uuid).first()

            files_path = os.path.join(settings.STORAGE_PATH, str(self.owner_id))

            file_path = os.path.join(files_path, self.file_uuid)
            self.frames_count = media_utils.get_video_frames_count(file_path)

            new_file_uuid = files_utils.generate_uuid()

            with files_utils.tmp_directory_scope(settings.TMP_PATH) as tmp_dir_path:
                output_path = os.path.join(tmp_dir_path, new_file_uuid)

                codec_subcommand = "-c:v libx264" if self.re_encode else "-c:v copy"
                command = f"ffmpeg -i {file_path} -movflags +faststart {codec_subcommand}" \
                          f" -c:a aac -f {file.extension} {output_path}"

                process = subprocess.Popen(command.split(),
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True)

                for row in process.stdout:
                    current_frame = self.get_current_processing_frame(row)

                    if current_frame:
                        self.calc_progress(current_frame, self.frames_count)
                        self.update_process_data()

                self.add_file(new_file_uuid, file.extension, output_path)

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
