from django.apps import AppConfig

class InteractionsConfig(AppConfig):
    """
    VIBEPLAY INTERACTIONS ENGINE
    Handles social engagement: Likes, Comments, and Following.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.interactions'
    label = 'interactions'

    def ready(self):
        # Kept empty to prevent circular imports during the initial registry load
        pass