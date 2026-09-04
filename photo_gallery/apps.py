from django.apps import AppConfig


class PhotoGalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photo_gallery'

    def ready(self):
        import photo_gallery.signals  # noqa: F401
