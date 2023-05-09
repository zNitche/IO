from django.conf import settings
import os


def make_files_dir_for_user(user_id):
    user_files_path = os.path.join(settings.FILES_DIR, str(user_id))

    if not os.path.exists(user_files_path):
        os.mkdir(user_files_path)


def get_size_of_file(file_path):
    file_stats = os.stat(file_path)

    return file_stats.st_size
