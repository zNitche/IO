"""io_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path("", include("io_app.apps.core.urls")),
    path("auth/", include("io_app.apps.authenticate.urls")),
    path("storage/", include("io_app.apps.storage_manager.urls")),
    path("api/", include("io_app.apps.api.urls")),
]


if settings.DEBUG or settings.ADMIN_ENABLED:
    from django.contrib import admin

    admin.site.site_header = "IO admin"
    admin.site.index_title = "IO admin"
    admin.site.site_title = "IO admin"

    urlpatterns.append(path('admin/', admin.site.urls))


handler404 = "io_app.apps.core.error_views.not_found"
handler500 = "io_app.apps.core.error_views.server_error"
handler400 = "io_app.apps.core.error_views.bad_request"
