from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'io_app.apps.files'
    label = 'files'

    def ready(self):
        from io_app.apps.files import signals
