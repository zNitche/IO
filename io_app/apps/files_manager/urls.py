from django.urls import path
from io_app.apps.files_manager.views import files_views, directories_views


app_name = "files_manager"

urlpatterns = [
    path("upload/", files_views.upload, name="upload"),
    path("upload_file/", files_views.upload_file, name="upload_file"),
    path("<str:file_uuid>/download/", files_views.download_file, name="download_file"),
    path("<str:file_uuid>/remove/", files_views.remove_file, name="remove_file"),
    path("<str:file_uuid>/preview/", files_views.preview_raw, name="preview_raw"),
    path("<str:file_uuid>/management/", files_views.file_management, name="file_management"),
    path("directories/add", directories_views.add_directory, name="add_directory"),
    path("directories/<str:directory_uuid>/management/", directories_views.directory_management, name="directory_management"),
    path("directories/<str:directory_uuid>/remove/", directories_views.remove_directory, name="remove_directory"),
]
