from django.apps import AppConfig


class AppUserConfig(AppConfig):
    name = 'users'

    def ready(self):
        import app_user.signal
