from django.apps import AppConfig


class MangaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manga'

class PaypalConfig(AppConfig):
    name = 'paypal'
