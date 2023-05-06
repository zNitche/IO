from django.urls import path
from io_app.apps.authenticate import views

app_name = "authenticate"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout")
]
