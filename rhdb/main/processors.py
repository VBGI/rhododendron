from .models import Page, Image, Record


def base(request):
    return {'pages': Page.objects.filter(public=True),
            'random_images': Image.objects.filter(public=True),
            'total': Record.objects.all().count()
            }