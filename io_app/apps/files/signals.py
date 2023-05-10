from django.db.models.signals import post_delete
from django.dispatch import receiver
from io_app.apps.files import models
from io_app.utils import files_utils


@receiver(post_delete, sender=models.File)
def remove_file(sender, instance, **kwargs):
    files_utils.remove_user_file(instance.owner_id, instance.uuid)
