from django.contrib import admin
from io_app.apps.files import admin_models, models


# Register your models here.
admin.site.register(models.File, admin_models.FilesAdmin)
