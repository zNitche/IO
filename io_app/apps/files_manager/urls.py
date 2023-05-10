from django.urls import path
from io_app.apps.files_manager import views


app_name = "files_manager"

urlpatterns = [
    path("upload/", views.upload, name="upload"),
    path("upload_file/", views.upload_file, name="upload_file"),
]
