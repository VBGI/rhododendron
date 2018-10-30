from django.contrib import admin

from .models import Species, Image, Record, Page, PhotoAlbum


class ImageAdminInline(admin.StackedInline):
    model = Image
    extra = 1

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    inlines = [ImageAdminInline]




# Register your models here.
admin.site.register((Species, Image, Page, PhotoAlbum))