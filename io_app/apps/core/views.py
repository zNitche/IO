from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from io_app.consts import PaginationConsts
from io_app.apps.files_manager import models


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
def my_directories(request, page_id=1):
    search_dir_name = request.GET.get("search_dir", "")

    directories = request.user.directories.filter(name__contains=search_dir_name).order_by("-creation_date").all()

    directories_paginator = Paginator(directories, PaginationConsts.FILES_PER_PAGE)
    directories_page = directories_paginator.get_page(page_id)

    return render(request, "directories.html", {
        "directories_page": directories_page,
        "search_dir_name": search_dir_name,
    })


@login_required
@require_http_methods(["GET"])
def directory_content(request, directory_uuid, page_id=1):
    directory = get_object_or_404(models.Directory, owner_id=request.user.id, uuid=directory_uuid)
    search_file_name = request.GET.get("search_file", "")

    files = directory.files.filter(name__contains=search_file_name).order_by("-upload_date").all()

    files_paginator = Paginator(files, PaginationConsts.FILES_PER_PAGE)
    files_page = files_paginator.get_page(page_id)

    return render(request, "directory.html", {
        "files_page": files_page,
        "search_file_name": search_file_name,
        "directory": directory,
    })
