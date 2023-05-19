from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from io_app.apps.storage_manager import models
from io_app.consts import MessagesConsts
from io_app.apps.storage_manager import forms
import logging


logger = logging.getLogger(settings.LOGGER_NAME)


@login_required
@require_http_methods(["GET", "POST"])
def add_directory(request):
    form = forms.AddDirectoryForm(data=request.POST or None)

    if request.method == "POST":
        form.user = request.user

        if form.is_valid():
            directory_name = request.POST["directory_name"]
            models.Directory(name=directory_name, owner=request.user).save()

            messages.add_message(request, messages.SUCCESS, MessagesConsts.DIRECTORY_ADDED)

            return redirect("core:directories")

    return render(request, "add_directory.html", {"form": form})


@login_required
@require_http_methods(["GET"])
def directory_management(request, directory_uuid):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid, owner=request.user)

    change_directory_name_form = forms.ChangeDirectoryNameForm()
    change_directory_name_form.fields["directory_name"].initial = directory.name

    update_files_form = forms.UpdateDirectoryFilesForm()
    directory_files = [(file.name, file.name) for file in directory.files.all()]
    all_files = [(file.name, file.name) for file in request.user.files.filter(directory=None).all()]

    update_files_form.fields["files"].choices = directory_files + all_files
    update_files_form.fields["files"].initial = [name[0] for name in directory_files]

    share_to_user_form = forms.ShareDirectoryToUserForm()
    share_to_user_form.user = request.user

    context = {
        "directory": directory,
        "update_files_form": update_files_form,
        "share_to_user_form": share_to_user_form,
        "change_directory_name_form": change_directory_name_form,
    }

    return render(request, "directory_management.html", context)


@login_required
@require_http_methods(["POST"])
def remove_directory(request, directory_uuid):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid, owner=request.user)
    directory.delete()

    messages.add_message(request, messages.SUCCESS, MessagesConsts.DIRECTORY_REMOVED_SUCCESSFULLY)

    return redirect("core:directories")


@login_required
@require_http_methods(["POST"])
def update_directory_files(request, directory_uuid):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid, owner=request.user)

    form = forms.UpdateDirectoryFilesForm(data=request.POST)
    form.user = request.user

    directory_files = [(file.name, file.name) for file in directory.files.all()]
    all_files = [(file.name, file.name) for file in request.user.files.filter(directory=None).all()]

    form.fields["files"].choices = directory_files + all_files

    if form.is_valid():
        files = request.POST.getlist("files")

        files_models = [file for file in request.user.files.all() if file.name in files]

        directory.files.set(files_models)
        directory.save()

        messages.add_message(request, messages.SUCCESS,
                             MessagesConsts.UPDATED_DIRECTORY_FILES.format(files_count=len(files_models)))

    return redirect("storage_manager:directory_management", directory_uuid=directory_uuid)


@login_required
@require_http_methods(["POST"])
def share_directory_to_user(request, directory_uuid):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid, owner=request.user)

    form = forms.ShareDirectoryToUserForm(data=request.POST)
    form.user = request.user

    if form.is_valid():
        username = request.POST["username"]
        user = get_user_model().objects.filter(username=username).first()

        if user not in directory.shared_to_users.all():
            user.shared_directories.add(directory)
            user.save()

            messages.add_message(request, messages.SUCCESS, MessagesConsts.SHARED_TO_USER.format(
                obj_name=directory.name, username=username))

        else:
            messages.add_message(request, messages.ERROR, MessagesConsts.DIRECTORY_ALREADY_SHARED_TO_USER)

    else:
        messages.add_message(request, messages.ERROR, MessagesConsts.ERROR_WHILE_SHARING_DIRECTORY_TO_USER)

    return redirect("storage_manager:directory_management", directory_uuid=directory_uuid)


@login_required
@require_http_methods(["POST"])
def remove_directory_from_shared(request, directory_uuid):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid, owner=request.user)

    username = request.POST["username"]
    user = get_user_model().objects.filter(username=username).first()

    if user:
        if user in directory.shared_to_users.all():
            user.shared_directories.remove(directory)
            user.save()

            messages.add_message(request, messages.SUCCESS, MessagesConsts.REMOVE_SHARED_TO_USER.format(
                obj_name=directory.name, username=user.username))

        else:
            messages.add_message(request, messages.ERROR, MessagesConsts.DIRECTORY_NOT_SHARED_TO_USER)
    else:
        messages.add_message(request, messages.ERROR, MessagesConsts.USER_DOESNT_EXIST)

    return redirect("storage_manager:directory_management", directory_uuid=directory_uuid)


@login_required
@require_http_methods(["POST"])
def directory_change_name(request, directory_uuid):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid, owner=request.user)

    form = forms.ChangeDirectoryNameForm(data=request.POST)
    form.user = request.user

    if form.is_valid():
        directory_name = request.POST["directory_name"]

        directory.name = directory_name
        directory.save()

        messages.add_message(request, messages.SUCCESS, MessagesConsts.CHANGED_DIRECTORY_NAME)

    else:
        messages.add_message(request, messages.ERROR, MessagesConsts.ERROR_WHILE_CHANGING_DIRECTORY_NAME)

    return redirect("storage_manager:directory_management", directory_uuid=directory_uuid)
