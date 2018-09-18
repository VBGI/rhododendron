# Generated by Django 2.0.7 on 2018-09-18 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180918_0041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photoalbum',
            old_name='category_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.PhotoAlbum', verbose_name='альбом'),
        ),
    ]
