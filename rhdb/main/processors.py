from .models import Page


def base(request):
    return {'pages': Page.objects.filter(public=True),
            }