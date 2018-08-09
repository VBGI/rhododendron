from django.contrib import admin

from .models import Species, Image, Record, Page


# Register your models here.
admin.site.register((Species, Image, Record, Page))