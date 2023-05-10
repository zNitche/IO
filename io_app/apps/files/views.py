from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from io_app.utils import files_utils
from io_app.apps.files import models
from io_app.consts import MessagesConsts
import uuid
import logging
import os


logger = logging.getLogger(settings.LOGGER_NAME)


@login_required
@require_http_methods(["GET"])
def upload_view(request):
    return render(request, "upload.html", {
        "upload_url": reverse("files:upload")
    })


@login_required
@require_http_methods(["POST"])
def upload(request):
    filename = request.headers["X-File-Name"]
    file_size = int(request.headers["X-File-Size"])
    file_extension = filename.split(".")[-1]

    files_utils.make_files_dir_for_user(request.user.id)

    file_uuid = str(uuid.uuid4().hex)
    file_path = os.path.join(settings.STORAGE_PATH, str(request.user.id), file_uuid)

    try:
        with open(file_path, "wb") as data:
            while True:
                file_chunk = request.read(settings.FILES_UPLOAD_CHUNK_LENGTH)

                if len(file_chunk) <= 0:
                    break

                data.write(file_chunk)

        uploaded_file_size = files_utils.get_size_of_file(file_path)

        if uploaded_file_size == file_size:
            models.File(name=filename, uuid=file_uuid, extension=file_extension,
                        size=uploaded_file_size,
                        owner_id=request.user.id).save()

            response_message = MessagesConsts.FILE_UPLOADED_SUCCESSFULLY.format(filename=filename)
            response_status = 200

        else:
            response_message = MessagesConsts.FILE_UPLOAD_FAILED_SIZE_MISMATCH
            response_status = 500

            logger.error(MessagesConsts.FILE_UPLOAD_FAILED_SIZE_MISMATCH_LOG.format(
                filename=filename, org_size=str(file_size), saved_size=str(uploaded_file_size))
            )

            files_utils.remove_user_file(request.user.id, file_uuid)

        response_data = {
            "message": response_message
        }

    except Exception as e:
        response_data = {
            "message": MessagesConsts.ERROR_WHILE_UPLOADING_FILE.format(filename=filename)
        }
        response_status = 500

        logger.error(MessagesConsts.ERROR_WHILE_UPLOADING_FILE_LOG.format(filename=filename, e=str(e)))

    finally:
        pass

    return JsonResponse(data=response_data, status=response_status)
