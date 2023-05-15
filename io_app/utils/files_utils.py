from django.conf import settings
import os
import uuid
from io_app.consts import MediaConsts


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

    if os.path.exists(user_files_path):
        for file in os.listdir(user_files_path):
            file_path = os.path.join(user_files_path, file)
            files_size += get_size_of_file(file_path)

    return files_size


def get_user_storage_size_in_mb(user_id):
    files_size = round((get_user_storage_size(user_id) / MediaConsts.BYTES_IN_MB), 2)

    return files_size


def get_used_storage_by_file_extension(user_files):
    storage_usage = {}

    for file in user_files:
        if file.extension not in storage_usage.keys():
            storage_usage[file.extension] = 0

        storage_usage[file.extension] += file.size

    return storage_usage


def get_used_storage_by_file_extension_percentage(user_id, user_files):
    storage_usage = get_used_storage_by_file_extension(user_files)
    total_storage_use = get_user_storage_size(user_id)

    storage_usage_percentage = {}

    for extension in storage_usage:
        if extension not in storage_usage.keys():
            storage_usage_percentage[extension] = 0

        storage_usage_percentage[extension] = round((storage_usage[extension] * 100 / total_storage_use), 2)

    return storage_usage_percentage


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


def generate_uuid():
    return str(uuid.uuid4().hex)
