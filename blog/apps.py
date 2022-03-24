from django.apps import AppConfig
from django.db.models.signals import post_migrate

class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from .models import auto_generate_day_pages
        post_migrate.connect(auto_generate_day_pages, sender=self)
        



