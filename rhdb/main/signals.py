
from .conf import settings
from .models import Image
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from PIL import Image as ImInstance
import os



@receiver(post_save, sender=Image)
def create_thumbnail(sender, instance, **kwargs):
    if instance.src:
        try:
            opened = ImInstance.open(instance.src)
        except IOError:
            return

        destination_file = \
                          settings.MEDIA_ROOT + os.path.join(instance.image_path,
                          settings.RHD_THUMBNAIL_DIR)
        if not os.path.exists(destination_file):
            os.mkdir(destination_file)
        destination_file = os.path.join(destination_file, instance.image_name)
        new_img = opened.resize((settings.RHD_THUMBNAIL_W,
                                 settings.RHD_THUMBNAIL_H))
        print("Destination file is ", destination_file)
        new_img.save(fp=open(destination_file, 'wb'), format='JPEG')



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