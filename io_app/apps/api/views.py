from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from io_app.utils import files_utils


@login_required
@require_http_methods(["GET"])
def storage_usage(request):
    used_space = files_utils.get_user_storage_size_in_mb(request.user.id)

    return JsonResponse(data={
        "free_space": round((request.user.private_storage_space - used_space), 2),
        "used_space": used_space
    })


@login_required
@require_http_methods(["GET"])
def storage_usage_by_filetype(request):
    storage_usage_percentage = files_utils.get_used_storage_by_file_extension_percentage(
        request.user.id,
        request.user.files.all()
    )

    return JsonResponse(data=storage_usage_percentage)
