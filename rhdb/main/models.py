# coding: utf-8
from django.db import models


class UpdaterMixin:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Species(models.Model, UpdaterMixin):
    name = models.CharField(max_length=50, default='',
                            blank=False, verbose_name='название вида')
    info = models.TextField(blank=True, default='', verbose_name='общая информация')


class Record(models.Model, UpdaterMixin):
    species = models.ForeignKey(Species, null=True, blank=False,
                                verbose_name='вид', on_delete=models.CASCADE)
    content = models.TextField(blank=True, default='',
                               verbose_name='содержимое страницы')
    region = models.CharField(blank=True, default='', verbose_name='регион',
                              max_length=70)
    district = models.CharField(blank=True, default='', verbose_name='район',
                                max_length=70)
    latitude = models.FloatField(null=True, verbose_name='широта')
    longitude = models.FloatField(null=True, verbose_name='долгота')


class Image(models.Model, UpdaterMixin):
    order = models.IntegerField(default=0, blank=True, verbose_name='порядок')
    src = models.ImageField(verbose_name='изображение', blank=False, null=True)
    record = models.ForeignKey(Record, null=True, blank=True,
                               verbose_name='запись', on_delete=models.CASCADE)
    title = models.CharField(default='', blank=True, verbose_name='название',
                             max_length=100)
    description = models.TextField(default='', blank=True,
                                   verbose_name='описание')



