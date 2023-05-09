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
    file_extension = filename.split(".")[-1]

    response_data = {
        "message": MessagesConsts.FILE_UPLOADED_SUCCESSFULLY.format(filename=filename)
    }
    response_status = 200

    files_utils.make_files_dir_for_user(request.user.id)

    file_uuid = str(uuid.uuid4().hex)
    file_path = os.path.join(settings.FILES_DIR, str(request.user.id), file_uuid)

    try:
        with open(file_path, "wb") as data:
            while True:
                file_chunk = request.read(settings.FILES_UPLOAD_CHUNK_LENGTH)

                if len(file_chunk) <= 0:
                    break

                data.write(file_chunk)

        models.File(name=filename, uuid=file_uuid, extension=file_extension,
                    size=files_utils.get_size_of_file(file_path),
                    owner_id=request.user.id).save()

    except Exception as e:
        response_data = {
            "message": MessagesConsts.ERROR_WHILE_UPLOADING_FILE.format(filename=filename)
        }
        response_status = 500

        logger.error(MessagesConsts.ERROR_WHILE_UPLOADING_FILE_LOG.format(filename=filename, e=str(e)))

    finally:
        pass

    return JsonResponse(data=response_data, status=response_status)
