from django.urls import path
from io_app.apps.core import views


app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("page/<str:page_id>/", views.home, name="home"),
]
