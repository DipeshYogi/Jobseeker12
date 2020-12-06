from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self): #for profile models to send signals to signal.py
        import users.signals
