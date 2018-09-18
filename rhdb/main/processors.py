from .models import Page, Image, Record
from .conf import settings

def base(request):
    return {'pages': Page.objects.filter(public=True),
            'random_images': Image.objects.filter(public=True),
            'total': Record.objects.all().count(),
            'album_url': settings.RHD_ALBUM_URL
            }