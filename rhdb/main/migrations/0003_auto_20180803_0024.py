# Generated by Django 2.0.7 on 2018-08-03 00:24

import ckeditor.fields
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180727_0433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='содержание')),
                ('title', models.CharField(blank=True, default='', max_length=50, verbose_name='название')),
            ],
            bases=(models.Model, main.models.UpdaterMixin),
        ),
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ('pk',), 'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterField(
            model_name='image',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, default='', verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='record',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, default='', verbose_name='содержимое страницы'),
        ),
        migrations.AlterField(
            model_name='species',
            name='info',
            field=ckeditor.fields.RichTextField(blank=True, default='', verbose_name='общая информация'),
        ),
    ]
