from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@login_required
@require_http_methods(["GET"])
def home(request):
    recent_files = request.user.files.order_by("-upload_date")[:5]
    files = request.user.files.order_by("-upload_date").all()

    return render(request, "home.html", {
        "recent_files": recent_files,
        "files": files,
    })
