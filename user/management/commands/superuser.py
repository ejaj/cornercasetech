import sys
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Class for create super user by command line
    """

    help = 'Creating superuser from environment'

    def handle(self, *args, **kwargs):

        user_obj = get_user_model()
        if os.environ.get('SUPERUSER_EMAIL', None):
            user_data = user_obj.objects.filter(email=os.environ.get('SUPERUSER_EMAIL', None))
            if user_data.exists():
                self.stdout.write("Username already exist in the system")
                sys.exit(0)
            else:
                try:
                    created_user = user_obj.objects.create_superuser(
                        os.environ.get('SUPERUSER_EMAIL', "kazi@gmail.com"),
                        os.environ.get('SUPERUSER_PASS', "kazi123456"),
                        is_staff=True,
                        is_active=True,
                        is_superuser=True
                    )
                    self.stdout.write(
                        self.style.SUCCESS('Superuser successfully created with username: %s' % created_user.email))
                except Exception as e:
                    self.stdout.write(self.style.ERROR('Error: %s' % (e,)))
        else:
            self.stdout.write(self.style.ERROR('Error: Environment is not setup properly'))
