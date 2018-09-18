
from .conf import settings
from .models import Image
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os


@receiver(post_save, sender=Image)
def create_thumbnail(sender, instance, **kwargs):
    if instance.src:
        #TODO: create image thmbnail using PILLOW library.
        pass


@receiver(post_delete, sender=Image)
def clean_files(sender, instance, **kwargs):
    if instance.src:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.image_path,
                                   instance.image_name))
        except:
            pass
        try:
            instance.src.delete(save=False)
        except:
            pass