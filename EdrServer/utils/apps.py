from django.apps import AppConfig
import os


class UtilsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utils'
        
    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
        # import utils.checks
