from django.contrib import admin
from io_app.apps.files_manager import admin_models, models


# Register your models here.
admin.site.register(models.File, admin_models.FilesAdmin)
admin.site.register(models.Directory, admin_models.DirectoryAdmin)
