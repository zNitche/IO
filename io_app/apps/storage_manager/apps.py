from django.apps import AppConfig


class FilesManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'io_app.apps.storage_manager'
    label = 'storage_manager'

    def ready(self):
        from io_app.apps.storage_manager import signals
