# Generated by Django 4.1.2 on 2023-05-24 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_album_date_rated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='type_owned',
            field=models.CharField(blank=True, choices=[('AC', 'Acheté'), ('TL', 'Téléchargé')], max_length=2, verbose_name='Type possédé'),
        ),
    ]
