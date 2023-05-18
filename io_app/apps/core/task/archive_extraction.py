from io_app.celery_tasks.user_task_base import UserTaskBase
from io_app.apps.storage_manager import models
from io_app.consts import ProcessesConsts


class ArchiveExtraction(UserTaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 60

        self.filename = ""

    def run(self, owner_id, filename):
        self.owner_id = owner_id
        self.filename = filename

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
            ProcessesConsts.FILENAME: self.filename,
        }

        return process_data

    def mainloop(self):
        self.update_process_data()

        try:
            self.logger.debug("Archive extraction process running...")

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()
