import os

from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import tempfile


@login_required
@require_http_methods(["GET"])
def upload_view(request):
    return render(request, "upload.html", {
        "upload_url": reverse("files:upload")
    })


@login_required
@require_http_methods(["POST"])
def upload(request):
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file_path = os.path.join(tempfile.tempdir, tmp_file.name)

        with open(tmp_file_path, "wb") as data:
            while True:
                file_chunk = request.read(4096)

                if len(file_chunk) <= 0:
                    break

                data.write(file_chunk)

        data = {
            "message": "ok"
        }

    return JsonResponse(data=data, status=200)
