from django.urls import path
from io_app.apps.storage_manager.views import files_views, directories_views


app_name = "storage_manager"

urlpatterns = [
    path("upload/", files_views.upload, name="upload"),
    path("upload_file/", files_views.upload_file, name="upload_file"),
    path("files/<str:file_uuid>/download/", files_views.download_file, name="download_file"),
    path("files/<str:file_uuid>/remove/", files_views.remove_file, name="remove_file"),
    path("files/<str:file_uuid>/preview/", files_views.preview_raw, name="preview_raw"),
    path("files/<str:file_uuid>/stream/", files_views.stream_media_file, name="stream_media_file"),
    path("files/<str:file_uuid>/management/", files_views.file_management, name="file_management"),
    path("files/<str:file_uuid>/change_directory/", files_views.change_directory, name="change_directory"),
    path("files/<str:file_uuid>/change_name/", files_views.file_change_name, name="file_change_name"),
    path("directories/add", directories_views.add_directory, name="add_directory"),
    path("directories/<str:directory_uuid>/management/", directories_views.directory_management,
         name="directory_management"),
    path("directories/<str:directory_uuid>/remove/", directories_views.remove_directory,
         name="remove_directory"),
    path("directories/<str:directory_uuid>/update_files/", directories_views.update_directory_files,
         name="update_directory_files"),
    path("directories/<str:directory_uuid>/share_directory_to_user/", directories_views.share_directory_to_user,
         name="share_directory_to_user"),
    path("directories/<str:directory_uuid>/remove_directory_from_shared/", directories_views.remove_directory_from_shared,
         name="remove_directory_from_shared"),
    path("directories/<str:directory_uuid>/change_name/", directories_views.directory_change_name,
         name="directory_change_name"),
]
