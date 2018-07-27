# Generated by Django 2.0.7 on 2018-07-27 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='image',
            name='src',
            field=models.ImageField(null=True, upload_to='', verbose_name='изображение'),
        ),
    ]
