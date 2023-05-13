from django.urls import path
from io_app.apps.core import views


app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("page/<str:page_id>/", views.home, name="home"),
    path("directories/", views.my_directories, name="directories"),
    path("directories/page/<str:page_id>/", views.my_directories, name="directories"),
    path("directories/<str:directory_uuid>/", views.directory_content, name="directory_content"),
    path("directories/<str:directory_uuid>/<str:page_id>/", views.directory_content, name="directory_content"),
]
