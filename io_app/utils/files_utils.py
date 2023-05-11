from django.conf import settings
import os


def make_files_dir_for_user(user_id):
    user_files_path = os.path.join(settings.STORAGE_PATH, str(user_id))

    if not os.path.exists(user_files_path):
        os.mkdir(user_files_path)


def get_size_of_file(file_path):
    file_stats = os.stat(file_path)

    return file_stats.st_size


def get_user_storage_size(user_id):
    user_files_path = os.path.join(settings.STORAGE_PATH, str(user_id))
    files_size = 0

    for file in os.listdir(user_files_path):
        file_path = os.path.join(user_files_path, file)
        files_size += get_size_of_file(file_path)

    return files_size


def remove_user_file(user_id, file_uuid):
    file_path = os.path.join(settings.STORAGE_PATH, str(user_id), file_uuid)

    if os.path.exists(file_path):
        os.remove(file_path)


def save_file_from_request(request, file_path):
    with open(file_path, "wb") as data:
        while True:
            file_chunk = request.read(settings.FILES_UPLOAD_CHUNK_LENGTH)

            if len(file_chunk) <= 0:
                break

            data.write(file_chunk)
