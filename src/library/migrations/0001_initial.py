# Generated by Django 4.1.2 on 2022-11-10 17:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='titre')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('date_released', models.DateField(blank=True, null=True, verbose_name='Date de sortie')),
                ('date_listened', models.DateField(blank=True, null=True, verbose_name="Date d'écoute")),
                ('date_added', models.DateField(auto_now=True, verbose_name="Date d'ajout")),
                ('type_vocal', models.CharField(choices=[('HA', 'Harsh'), ('CL', 'Clean'), ('MX', 'Mixed')], max_length=2, null=True, verbose_name='Voix')),
                ('type_album', models.CharField(choices=[('LP', 'LP'), ('EP', 'EP')], max_length=2, verbose_name='Type')),
                ('type_owned', models.CharField(blank=True, choices=[('VY', 'Vynile'), ('NU', 'Numérique'), ('CD', 'CD'), ('K7', 'K7')], max_length=2, verbose_name='Type possédé')),
                ('owned', models.BooleanField(default=False, verbose_name='Possédé')),
                ('rating', models.FloatField(blank=True, null=True, verbose_name='Note')),
                ('thumbnail', models.ImageField(blank=True, upload_to='albums')),
            ],
            options={
                'verbose_name': 'Album',
            },
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('country', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('date_added', models.DateField(auto_now=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='bands')),
            ],
            options={
                'verbose_name': 'Groupe',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Genre',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField()),
                ('type', models.CharField(choices=[('G', 'Genre'), ('Y', 'Année'), ('T', 'Top 10'), ('F', '5 Étoiles')], max_length=2)),
                ('optional', models.BooleanField(default=False, verbose_name='Optionel')),
            ],
            options={
                'verbose_name': 'Playlist',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('number', models.IntegerField(verbose_name='Numéro')),
                ('featuring_artist', models.CharField(blank=True, max_length=50, null=True, verbose_name='featuring')),
                ('duration', models.DurationField(verbose_name='durée')),
                ('favorite', models.BooleanField(blank=True, default=False, verbose_name='favori')),
                ('date_added', models.DateField(auto_now=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Note')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.album')),
                ('playlist', models.ManyToManyField(blank=True, null=True, related_name='playlist', to='library.playlist')),
            ],
            options={
                'verbose_name': 'Morceau',
                'ordering': ['number'],
            },
        ),
        migrations.AddField(
            model_name='album',
            name='genre_primary',
            field=models.ManyToManyField(related_name='primary_genre', to='library.genre', verbose_name='Genre Primaire'),
        ),
        migrations.AddField(
            model_name='album',
            name='genre_secondary',
            field=models.ManyToManyField(blank=True, related_name='secondary_genre', to='library.genre', verbose_name='Genre Secondaire'),
        ),
        migrations.AddField(
            model_name='album',
            name='groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.band'),
        ),
    ]
