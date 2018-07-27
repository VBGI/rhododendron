from django.contrib import admin

from .models import Species, Image, Record


# Register your models here.
admin.site.register((Species, Image, Record))