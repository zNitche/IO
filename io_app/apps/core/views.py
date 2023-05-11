from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from io_app.consts import PaginationConsts


@login_required
@require_http_methods(["GET"])
def home(request, page_id=1):
    files = request.user.files.order_by("-upload_date").all()
    recent_files = files[:5]

    files_paginator = Paginator(files, PaginationConsts.FILES_PER_PAGE)
    files_page = files_paginator.get_page(page_id)

    return render(request, "home.html", {
        "recent_files": recent_files,
        "files_page": files_page,
    })
