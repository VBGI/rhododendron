# Generated by Django 2.0.7 on 2018-09-19 04:21

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, default=0, verbose_name='порядок')),
                ('src', models.ImageField(null=True, upload_to='images/%Y/%m/%d/', verbose_name='изображение')),
                ('title', models.CharField(blank=True, default='', max_length=100, verbose_name='название')),
                ('description', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='описание')),
                ('public', models.BooleanField(default=False, verbose_name='опубликовать')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='содержание')),
                ('title', models.CharField(blank=True, default='', max_length=50, verbose_name='название')),
                ('public', models.BooleanField(default=False)),
                ('slug', models.CharField(blank=True, default='', max_length=10, verbose_name='путь')),
                ('order', models.IntegerField(blank=True, default=0)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
            },
        ),
        migrations.CreateModel(
            name='PhotoAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=300)),
                ('slug', models.CharField(default='', max_length=20)),
                ('child', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='main.PhotoAlbum')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='содержимое страницы')),
                ('region', models.CharField(blank=True, default='', max_length=70, verbose_name='регион')),
                ('district', models.CharField(blank=True, default='', max_length=70, verbose_name='район')),
                ('latitude', models.FloatField(blank=True, default=0, null=True, verbose_name='широта')),
                ('longitude', models.FloatField(blank=True, default=0, null=True, verbose_name='долгота')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='название вида')),
                ('info', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='общая информация')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Вид',
                'verbose_name_plural': 'Виды',
            },
        ),
        migrations.AddField(
            model_name='record',
            name='species',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Species', verbose_name='вид'),
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.PhotoAlbum', verbose_name='альбом'),
        ),
        migrations.AddField(
            model_name='image',
            name='record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Record', verbose_name='запись'),
        ),
    ]
