from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from io_app.consts import PaginationConsts, MessagesConsts, MediaConsts
from io_app.apps.storage_manager import models
from io_app.apps.core import forms
from io_app.utils import processes_utils, files_utils


@login_required
@require_http_methods(["GET"])
def home(request, page_id=1):
    search_file_name = request.GET.get("search_file", "")

    files = request.user.files.filter(name__contains=search_file_name).order_by("-upload_date").all()
    recent_files = request.user.files.order_by("-upload_date").all()[:5]

    files_paginator = Paginator(files, PaginationConsts.FILES_PER_PAGE)
    files_page = files_paginator.get_page(page_id)

    return render(request, "home.html", {
        "recent_files": recent_files,
        "files_page": files_page,
        "search_file_name": search_file_name,
    })


@login_required
@require_http_methods(["GET"])
def directories(request, page_id=1):
    search_dir_name = request.GET.get("search_dir", "")

    directories = request.user.directories.filter(name__contains=search_dir_name).order_by("-creation_date").all()

    directories_paginator = Paginator(directories, PaginationConsts.FILES_PER_PAGE)
    directories_page = directories_paginator.get_page(page_id)

    return render(request, "directories.html", {
        "title": "My Directories",
        "directories_page": directories_page,
        "search_dir_name": search_dir_name,
    })


@login_required
@require_http_methods(["GET"])
def directory_content(request, directory_uuid, page_id=1):
    directory = get_object_or_404(models.Directory, uuid=directory_uuid)

    if request.user == directory.owner or request.user in directory.shared_to_users.all():
        search_file_name = request.GET.get("search_file", "")

        files = directory.files.filter(name__contains=search_file_name).order_by("-upload_date").all()

        files_paginator = Paginator(files, PaginationConsts.FILES_PER_PAGE)
        files_page = files_paginator.get_page(page_id)

        return render(request, "directory.html", {
            "files_page": files_page,
            "search_file_name": search_file_name,
            "directory": directory,
            "shared_view": False if request.user == directory.owner else True,
        })

    raise Http404


@login_required
@require_http_methods(["GET"])
def shared_directories(request, page_id=1):
    search_dir_name = request.GET.get("search_dir", "")

    directories = request.user.shared_directories.filter(name__contains=search_dir_name).order_by("-creation_date").all()

    directories_paginator = Paginator(directories, PaginationConsts.FILES_PER_PAGE)
    directories_page = directories_paginator.get_page(page_id)

    return render(request, "directories.html", {
        "title": "Shared Directories",
        "directories_page": directories_page,
        "search_dir_name": search_dir_name,
        "shared_view": True,
    })


@login_required
@require_http_methods(["GET"])
def processes(request):
    return render(request, "processes.html", {})


@login_required
@require_http_methods(["GET", "POST"])
def start_archive_extraction_process(request):
    form = forms.StartArchiveExtractionProcessForm(data=request.POST or None)
    form.user = request.user

    files = models.File.objects.filter(owner=request.user, directory=None).all()
    form.fields["file_name"].choices = [(file.name, file.name) for file in files]

    if request.method == "POST":
        if form.is_valid():
            file_name = form.cleaned_data["file_name"]

            file = models.File.objects.filter(owner=request.user, name=file_name).first()

            if files_utils.check_if_user_have_enough_space_for_file(request.user, file.size):
                processes_utils.start_file_process_for_user(request.user.id, "ArchiveExtraction", file.uuid)
                messages.add_message(request, messages.SUCCESS, MessagesConsts.PROCESS_STARTED_SUCCESSFULLY)

                return redirect("core:processes")

            else:
                messages.add_message(request, messages.ERROR, MessagesConsts.NOT_ENOUGH_STORAGE_FOR_OPERATION)

    return render(request, "start_process.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def start_directory_compression_process(request):
    form = forms.StartDirectoryCompressionProcessForm(data=request.POST or None)
    form.user = request.user

    directories = models.Directory.objects.filter(owner=request.user).all()
    form.fields["directory_name"].choices = [(directory.name, directory.name) for directory in directories]

    if request.method == "POST":
        if form.is_valid():
            directory_name = form.cleaned_data["directory_name"]
            directory = models.Directory.objects.filter(owner=request.user, name=directory_name).first()

            directory_size = sum([file.size for file in directory.files.all()])

            if files_utils.check_if_user_have_enough_space_for_file(request.user, directory_size):
                processes_utils.start_file_process_for_user(request.user.id, "DirectoryCompression", directory.uuid)
                messages.add_message(request, messages.SUCCESS, MessagesConsts.PROCESS_STARTED_SUCCESSFULLY)

                return redirect("core:processes")

            else:
                messages.add_message(request, messages.ERROR, MessagesConsts.NOT_ENOUGH_STORAGE_FOR_OPERATION)

    return render(request, "start_process.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def start_video_compatibility_conversion_process(request):
    form = forms.StartVideoCompatibilityConversionProcessForm(data=request.POST or None)
    form.user = request.user

    files = models.File.objects.filter(owner=request.user).all()
    form.fields["file_name"].choices = \
        [(file.name, file.name) for file in files if file.extension in MediaConsts.COMMON_VIDEO_EXTENSIONS]

    if request.method == "POST":
        if form.is_valid():
            file_name = form.cleaned_data["file_name"]
            re_encode = form.cleaned_data["re_encode"]
            file = models.File.objects.filter(owner=request.user, name=file_name).first()

            if files_utils.check_if_user_have_enough_space_for_file(request.user, file.size):
                processes_utils.start_file_process_for_user(request.user.id, "VideoCompatibilityConversion", file.uuid, {
                    "re_encode": re_encode,
                })

                messages.add_message(request, messages.SUCCESS, MessagesConsts.PROCESS_STARTED_SUCCESSFULLY)

                return redirect("core:processes")

            else:
                messages.add_message(request, messages.ERROR, MessagesConsts.NOT_ENOUGH_STORAGE_FOR_OPERATION)

    return render(request, "start_process.html", {"form": form})
