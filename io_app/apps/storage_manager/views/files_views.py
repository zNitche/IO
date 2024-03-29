from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse
from django.conf import settings
from django.contrib import messages
from io_app.utils import files_utils, common_utils
from io_app.apps.storage_manager import models
from io_app.consts import MessagesConsts, MediaConsts
from io_app.apps.storage_manager import forms
import logging
import os
import re


logger = logging.getLogger(settings.LOGGER_NAME)


@login_required
@require_http_methods(["GET"])
def upload(request):
    return render(request, "upload.html", {
        "upload_url": reverse("storage_manager:upload_file")
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


@require_http_methods(["GET"])
def preview(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid)

    if file.accessible_via_link or file.owner == request.user or file.check_if_shared_to_user(request.user):
        context = {
            "file": file,
        }

        return render(request, "file_preview.html", context)

    else:
        raise Http404


@require_http_methods(["GET"])
def download_file(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid)

    if file.accessible_via_link or file.owner == request.user or file.check_if_shared_to_user(request.user):
        file_path = os.path.join(settings.STORAGE_PATH, str(file.owner.id), file.uuid)

        return common_utils.send_file(file_path, file.name)

    else:
        raise Http404


@login_required
@require_http_methods(["POST"])
def remove_file(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)
    file.delete()

    messages.add_message(request, messages.SUCCESS, MessagesConsts.FILE_REMOVED_SUCCESSFULLY)

    return redirect("core:home")


@login_required
@require_http_methods(["POST"])
def toggle_access_via_link(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)
    file.accessible_via_link = not file.accessible_via_link
    file.save()

    messages.add_message(request, messages.SUCCESS, MessagesConsts.ACCESS_VIA_LINK_CHANGED)

    return redirect("storage_manager:file_management", file_uuid=file_uuid)


@login_required
@require_http_methods(["GET"])
def file_management(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)

    change_file_name_form = forms.ChangeFileNameForm(None)
    change_file_name_form.fields["file_name"].initial = file.name

    change_directory_form = forms.ChangeDirectoryForm(None)

    user_directories = [(directory.name, directory.name) for directory in request.user.directories.all()]
    user_directories.append(("root", "root"))

    change_directory_form.fields["directory_name"].choices = user_directories
    change_directory_form.fields["directory_name"].initial = [file.directory.name] if file.directory else ["root"]

    context = {
        "file": file,
        "change_directory_form": change_directory_form,
        "change_file_name_form": change_file_name_form,
    }

    return render(request, "file_management.html", context)


@require_http_methods(["GET"])
def preview_raw(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid)

    if file.accessible_via_link or file.owner == request.user or file.check_if_shared_to_user(request.user):
        file_path = os.path.join(settings.STORAGE_PATH, str(file.owner.id), file.uuid)
        media_extensions = MediaConsts.COMMON_VIDEO_EXTENSIONS + MediaConsts.COMMON_AUDIO_EXTENSIONS

        if file.extension in media_extensions:
            return render(request, "media_player.html", {"file": file})

        else:
            return common_utils.send_file(file_path, file.name, as_attachment=False)
    else:
        raise Http404


@require_http_methods(["GET"])
def stream_media_file(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid)

    if file.accessible_via_link or file.owner == request.user or file.check_if_shared_to_user(request.user):
        media_extensions = MediaConsts.COMMON_VIDEO_EXTENSIONS + MediaConsts.COMMON_AUDIO_EXTENSIONS

        if file.extension in media_extensions:
            range_header = request.headers.get("range")

            if range_header:
                file_path = os.path.join(settings.STORAGE_PATH, str(file.owner.id), file.uuid)
                file_size = files_utils.get_size_of_file(file_path)

                chunk_start = int(re.sub("\D", "", range_header))
                chunk_end = min(chunk_start + settings.MEDIA_FILE_STREAMING_CHUNK_SIZE, file_size - 1)

                headers = {
                    "Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": chunk_end - chunk_start + 1,
                    "Content-Type": "video/mp4",
                }

                file_chunk = files_utils.get_file_chunk(file_path, chunk_start, settings.MEDIA_FILE_STREAMING_CHUNK_SIZE)

                return HttpResponse(file_chunk, headers=headers, status=206)

    raise Http404


@login_required
@require_http_methods(["POST"])
def change_directory(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)
    form = forms.ChangeDirectoryForm(data=request.POST)
    form.user = request.user

    user_directories = [(directory.name, directory.name) for directory in request.user.directories.all()]
    user_directories.append(("root", "root"))
    form.fields["directory_name"].choices = user_directories

    if form.is_valid():
        directory_name = form.cleaned_data["directory_name"]

        if directory_name != "root":
            directory = models.Directory.objects.filter(name=directory_name, owner=request.user).first()
        else:
            directory = None

        file.directory = directory
        file.save()

        messages.add_message(request, messages.SUCCESS, MessagesConsts.DIRECTORY_CHANGED)

    return redirect("storage_manager:file_management", file_uuid=file_uuid)


@login_required
@require_http_methods(["POST"])
def file_change_name(request, file_uuid):
    file = get_object_or_404(models.File, uuid=file_uuid, owner=request.user)

    form = forms.ChangeFileNameForm(data=request.POST)
    form.user = request.user

    if form.is_valid():
        file_name = form.cleaned_data["file_name"]

        file.name = file_name
        file.save()

        messages.add_message(request, messages.SUCCESS, MessagesConsts.CHANGED_FILE_NAME)

    else:
        messages.add_message(request, messages.ERROR, MessagesConsts.ERROR_WHILE_CHANGING_FILE_NAME)

    return redirect("storage_manager:file_management", file_uuid=file_uuid)
