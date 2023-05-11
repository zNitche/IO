from django.urls import path
from io_app.apps.files_manager import views


app_name = "files_manager"

urlpatterns = [
    path("upload/", views.upload, name="upload"),
    path("upload_file/", views.upload_file, name="upload_file"),
    path("<str:file_uuid>/download/", views.download, name="download_file"),
    path("<str:file_uuid>/remove/", views.remove, name="remove_file"),
    path("<str:file_uuid>/preview/", views.preview_raw, name="preview_raw"),
]