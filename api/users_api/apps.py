from django.apps import AppConfig


class UsersApiConfig(AppConfig):
    name = 'users_api'

    def ready(self):
        import users_api.signal # noqa