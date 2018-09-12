# coding: utf-8
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

class UpdaterMixin:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# Create your models here.
class Species(models.Model, UpdaterMixin):
    name = models.CharField(max_length=50, default='',
                            blank=False, verbose_name='название вида')
    info = RichTextField(blank=True, default='', verbose_name='общая информация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'
        ordering = ('pk',)


class Record(models.Model, UpdaterMixin):
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


class Image(models.Model, UpdaterMixin):
    order = models.IntegerField(default=0, blank=True, verbose_name='порядок')
    src = models.ImageField(verbose_name='изображение', blank=False, null=True)
    record = models.ForeignKey(Record, null=True, blank=True,
                               verbose_name='запись', on_delete=models.CASCADE)
    title = models.CharField(default='', blank=True, verbose_name='название',
                             max_length=100)
    description = RichTextField(default='', blank=True, verbose_name='описание')
    public = models.BooleanField(default=False, blank=True, verbose_name='опубликовать')
    category = models.ForeignKey('self', related_name='parent', null=True, blank=True,
                                 on_delete=models.CASCADE)
    category_name = models.CharField(default='', blank=True, max_length=300)
    category_slug = models.CharField(default='', blank=True, max_length=8)

    def __str__(self):
        return self.title if self.title else self.description if self.description else self.pk

    def get_children(self):
        '''Return queryset of all descendants related with the current object'''
        return self.objects.all() # TODO: Fake function

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ('pk',)

class Page(models.Model, UpdaterMixin):
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




# TODO:  Image post save and post delete signals that create thumbnails are needed....
