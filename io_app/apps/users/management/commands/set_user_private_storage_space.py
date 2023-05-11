from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "set user private storage space"

    def handle(self, *args, **options):
        username = input("username: ")
        user = get_user_model().objects.filter(username=username).first()

        if user:
            self.stdout.write(self.style.SUCCESS(f"private space of '{user.username}': "
                                                 f"{user.private_storage_space} MB"))
            self.stdout.write(self.style.SUCCESS(f"set new storage space (in MB)"))

            new_space = int(input(">"))

            user.private_storage_space = new_space
            user.save()
        else:
            self.stdout.write(self.style.ERROR("user doesn't exist"))
