from django.apps import AppConfig
from django.db.models.signals import post_migrate

USERNAME = 'admin'
PASSWORD = '12345'


def create_admin(**kwargs):
    from django.contrib.auth import models as auth_models
    try:
        auth_models.User.objects.get(username=USERNAME)
    except auth_models.User.DoesNotExist:
        auth_models.User.objects.create_superuser(USERNAME, 'test@mail.com', PASSWORD)
    print(auth_models.User.objects.all())


class MemberAppConfig(AppConfig):
    name = 'member'

    def ready(self):
        post_migrate.connect(create_admin)
