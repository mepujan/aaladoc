from django.apps import AppConfig


class SitecontentsConfig(AppConfig):
    name = 'SiteContents'

    def ready(self):
        import SiteContents.signals
