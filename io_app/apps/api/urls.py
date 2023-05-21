from django.urls import path
from io_app.apps.api import views


app_name = "api"

urlpatterns = [
    path("storage_usage/", views.storage_usage, name="storage_usage"),
    path("storage_usage_by_filetype/", views.storage_usage_by_filetype, name="storage_usage_by_filetype"),
    path("processes/<str:user_id>/currently_running", views.running_processes_for_user,
         name="running_processes_for_user"),
]
