from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    label = 'users'

    def ready(self):
        # We MUST import signals inside ready()
        # but ONLY when the registry is fully loaded.
        try:
            import apps.users.signals
        except ImportError:
            pass