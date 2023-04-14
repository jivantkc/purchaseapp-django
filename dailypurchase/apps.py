from django.apps import AppConfig


class DailypurchaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dailypurchase'

    def ready(self):
        import api.signals