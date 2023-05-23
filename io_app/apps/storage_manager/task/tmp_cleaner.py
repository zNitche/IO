from django.conf import settings
from io_app.celery_tasks.background_task_base import BackgroundTaskBase
import os
import shutil


class TmpCleanerProcess(BackgroundTaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 60

        self.storage_path = settings.TMP_PATH

    def run(self):
        if not self.check_if_same_task_running():
            self.process_cache_key = f"{self.get_process_name()}_{self.timestamp}"
            self.mainloop()

        else:
            self.logger.info(f"[{self.get_process_name()}] - skipped, already running")

    def mainloop(self):
        try:
            self.update_process_data()

            for file in os.listdir(self.storage_path):
                if not file.startswith("."):
                    file_path = os.path.join(self.storage_path, file)

                    if os.path.exists(file_path):
                        if not os.path.isdir(file_path):
                            os.remove(file_path)
                        else:
                            shutil.rmtree(file_path)

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
