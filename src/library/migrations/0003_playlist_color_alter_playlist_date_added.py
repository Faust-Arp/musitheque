# Generated by Django 4.1.2 on 2022-11-17 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_playlist_date_added_playlist_fan_playlist_like_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='color',
            field=models.CharField(blank=True, max_length=7, verbose_name='Couleur'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='date_added',
            field=models.DateField(auto_now=True, null=True, verbose_name='Ajoutée le'),
        ),
    ]
