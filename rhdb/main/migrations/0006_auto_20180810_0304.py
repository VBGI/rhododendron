# Generated by Django 2.0.7 on 2018-08-10 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180810_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.CharField(default='', max_length=10, verbose_name='путь'),
        ),
    ]
