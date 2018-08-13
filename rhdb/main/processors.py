from .models import Page, Image


def base(request):
    return {'pages': Page.objects.filter(public=True),
            'random_images': Image.objects.filter(public=True)
            }