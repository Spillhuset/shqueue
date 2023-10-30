from django.apps import AppConfig


class SHqueueConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'apps.shqueue'

  def ready(self): #
    import apps.shqueue.signals
