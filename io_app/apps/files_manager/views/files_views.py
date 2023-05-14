from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from io_app.utils import files_utils, common_utils
from io_app.apps.files_manager import models
from io_app.consts import MessagesConsts, MediaConsts
import logging
import os


logger = logging.getLogger(settings.LOGGER_NAME)


@login_required
@require_http_methods(["GET"])
def upload(request):
    return render(request, "upload.html", {
        "upload_url": reverse("files_manager:upload_file")
    })


@login_required
@require_http_methods(["POST"])
def upload_file(request):
    filename = request.headers["X-File-Name"].replace("/", "-")
    file_size = int(request.headers["X-File-Size"])
    file_extension = filename.split(".")[-1].lower()

    files_utils.make_files_dir_for_user(request.user.id)

    file_uuid = files_utils.generate_uuid()
    file_path = os.path.join(settings.STORAGE_PATH, str(request.user.id), file_uuid)

    user_storage_size = files_utils.get_user_storage_size(request.user.id)
    file_with_same_name_exists = True if models.File.objects.filter(name=filename, owner=request.user).first() else False

    if file_with_same_name_exists:
        response_data = {
            "message": MessagesConsts.ERROR_WHILE_UPLOADING_FILE_EXISTS.format(filename=filename)
        }
        response_status = 200

    else:
        if (file_size + user_storage_size) <= request.user.get_private_storage_space():
            try:
                files_utils.save_file_from_request(request, file_path)
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

        else:
            response_data = {
                "message": MessagesConsts.ERROR_WHILE_UPLOADING_FILE_NO_SPACE.format(filename=filename)
            }
            response_status = 500

    return JsonResponse(data=response_data, status=response_status)


@login_required
@require_http_methods(["GET"])
def download_file(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)
    file_path = os.path.join(settings.STORAGE_PATH, str(request.user.id), file.uuid)

    return common_utils.send_file(file_path, file.name)


@login_required
@require_http_methods(["POST"])
def remove_file(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)
    file.delete()

    messages.add_message(request, messages.SUCCESS, MessagesConsts.FILE_REMOVED_SUCCESSFULLY)

    return redirect("core:home")


@login_required
@require_http_methods(["GET"])
def file_management(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)

    context = {
        "file": file,
    }

    return render(request, "file_management.html", context)


@login_required
@require_http_methods(["GET"])
def preview_raw(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)
    file_path = os.path.join(settings.STORAGE_PATH, str(request.user.id), file.uuid)

    if file.extension in MediaConsts.COMMON_AUDIO_EXTENSIONS or file.extension in MediaConsts.COMMON_VIDEO_EXTENSIONS:
        return common_utils.serve_media_file(file_path, file.name)

    else:
        return common_utils.send_file(file_path, file.name, as_attachment=False)
