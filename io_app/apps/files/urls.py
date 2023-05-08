from django.urls import path
from io_app.apps.files import views


app_name = "files"

urlpatterns = [
    path("upload_view/", views.upload_view, name="upload_view"),
    path("upload/", views.upload, name="upload"),
]
