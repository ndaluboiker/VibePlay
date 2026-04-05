from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """
    VIBEPLAY ANALYTICS ENGINE
    Handles tracking of views, watch time, and creator performance.
    """
    # Sets the primary key type for all models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # The full path to the folder
    name = 'apps.analytics'

    # The short label used in database relationships
    label = 'analytics'

    def ready(self):
        """
        Runs when the Django Registry is fully loaded.
        We keep this empty for now to prevent early-import crashes.
        """
        pass