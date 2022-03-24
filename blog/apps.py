from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from .models import auto_generate_day_pages
        auto_generate_day_pages()



