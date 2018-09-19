# coding: utf-8
from django.db import models
from ckeditor.fields import RichTextField
from .conf import settings
from django.urls import reverse
import os

class UpdaterMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Species(UpdaterMixin):
    name = models.CharField(max_length=50, default='',
                            blank=False, verbose_name='название вида')
    info = RichTextField(blank=True, default='', verbose_name='общая информация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'
        ordering = ('pk',)
        



class Record(UpdaterMixin):
    species = models.ForeignKey(Species, null=True, blank=False,
                                verbose_name='вид', on_delete=models.CASCADE)
    content = RichTextField(blank=True, default='',
                            verbose_name='содержимое страницы')
    region = models.CharField(blank=True, default='', verbose_name='регион',
                              max_length=70)
    district = models.CharField(blank=True, default='', verbose_name='район',
                                max_length=70)
    latitude = models.FloatField(null=True, verbose_name='широта',
                                 blank=True, default=0)
    longitude = models.FloatField(null=True, verbose_name='долгота',
                                  blank=True, default=0)

    def __str__(self):
        #FIXME: ugly string...
        return ((self.species.name if self.species else ' ') +
                self.region + ' ' + self.district).strip()

    def get_absolute_url(self):
        return reverse('record-info', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ('pk',)
        


class PhotoAlbum(UpdaterMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = []

    parent = models.ForeignKey('self', related_name='children',
                              null=True, blank=True,
                              on_delete=models.CASCADE,
                               verbose_name='родитель')
    name = models.CharField(default='', blank=True, max_length=300,
                            verbose_name='название')
    slug = models.CharField(default='', blank=False, max_length=20,
                            verbose_name='идентификатор')

    def get_children(self):
        """Gets all child albums for the current one"""
        visited = []
        unvisited = [self]
        def walk_recursively(unvisited):
            if unvisited:
                to_append = []
                while unvisited:
                    item = unvisited.pop()
                    visited.append(item)
                    to_append += [x for x in item.children.all()]
                unvisited += to_append
                walk_recursively(unvisited)

        walk_recursively(unvisited)
        return visited

    def get_images(self):
        """Gets all images in the current album"""

        return Image.objects.filter(album=self).order_by('order')

    def get_all_images(self):
        """Gets all images in the current album and its descendants"""

        result = []
        for obj in self.get_children():
            result += list(obj.get_images())
        return result

    def __str__(self):
        return (self.name or self.pk) + ' |'+ str(self.created.strftime("%Y-%m-%d-%H:%M:%S"));

    class Meta:
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'


class Image(UpdaterMixin):
    order = models.IntegerField(default=0, blank=True, verbose_name='порядок')
    src = models.ImageField(verbose_name='изображение', blank=False, null=True,
                            upload_to='images/%Y/%m/%d/')
    record = models.ForeignKey(Record, null=True, blank=True,
                               verbose_name='запись', on_delete=models.CASCADE)
    title = models.CharField(default='', blank=True, verbose_name='название',
                             max_length=100)
    description = RichTextField(default='', blank=True, verbose_name='описание')
    public = models.BooleanField(default=False, blank=True, verbose_name='опубликовать')

    album = models.ForeignKey('PhotoAlbum', null=True, blank=True,
                              verbose_name='альбом', on_delete=models.CASCADE)
    @property
    def image_name(self):
        if self.src:
            return os.path.basename(self.src.path)
        else:
            return ''

    @property
    def image_path(self): #TODO : not working
        '''Gets relative to MEDIA_ROOT image path'''

        if self.src:
            s = self.src.path
            s = s.replace(self.image_name, '')
            s = s.replace(settings.MEDIA_ROOT, '')
            print("Getting the value", s)
            print("Current media_root", settings.MEDIA_ROOT)
            return s
        else:
            return ''

    def get_thumbnail_url(self):
        if self.src:
            return settings.MEDIA_URL + os.path.join(self.image_path, settings.RHD_THUMBNAIL_DIR,
                                self.image_name)
        else:
            return ''

    def get_absolute_url(self):
        return settings.MEDIA_URL + os.path.join(self.image_path, self.image_name)

    def __str__(self):
        return self.title if self.title else self.description if self.description else str(self.pk)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ('pk',)
        

class Page(UpdaterMixin):
    content = RichTextField(default='', blank=True,
                            verbose_name='содержание')
    title = models.CharField(default='', blank=True, verbose_name='название',
                             max_length=50)
    public = models.BooleanField(default=False, blank=True)
    slug = models.CharField(default='', verbose_name='путь', max_length=10,
                            blank=True)
    order = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title if self.title else self.pk

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ('order',)
        

    def get_absolute_url(self):
        if self.slug.strip() == '/':
            return reverse('base-view')
        elif self.slug:
            return reverse('base-view') + self.slug
        else:
            return reverse('page-info', kwargs={'pk': self.pk})
