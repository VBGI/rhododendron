from django.contrib import admin

from .models import Species, Image, Record, Page, PhotoAlbum


# Register your models here.
admin.site.register((Species, Image, Record, Page, PhotoAlbum))