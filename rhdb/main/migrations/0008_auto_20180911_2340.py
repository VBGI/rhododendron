# Generated by Django 2.0.7 on 2018-09-11 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20180813_0229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ('order',), 'verbose_name': 'Страница', 'verbose_name_plural': 'Страницы'},
        ),
        migrations.AddField(
            model_name='page',
            name='order',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
