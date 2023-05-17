from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from io_app.consts import PaginationConsts
from io_app.apps.storage_manager import models


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
