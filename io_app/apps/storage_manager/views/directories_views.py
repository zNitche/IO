from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
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

    context = {
        "directory": directory,
    }

    return render(request, "directory_management.html", context)


@login_required
@require_http_methods(["POST"])
def remove_directory(request, directory_uuid):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid, owner=request.user)
    directory.delete()

    messages.add_message(request, messages.SUCCESS, MessagesConsts.DIRECTORY_REMOVED_SUCCESSFULLY)

    return redirect("core:directories")
