from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Band(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now=True)
    thumbnail = models.ImageField(blank=True, upload_to='bands')

    class Meta:
        verbose_name = "Groupe"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('library:home')


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = "Genre"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Album(models.Model):

    ALBUM_TYPE_CHOICES = [
        ("LP", "LP"),
        ("EP", "EP")]

    VOICE_STYLE_CHOICES = [
        ("HA", "Harsh"),
        ("CL", "Clean"),
        ("MX", "Mixed")
    ]

    TYPE_OWNED_CHOICES = [
        ("VY", "Vynile"),
        ("NU", "Numérique"),
        ("CD", "CD"),
        ("K7", "K7")
    ]

    title = models.CharField(max_length=50, verbose_name="titre")
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    groupe = models.ForeignKey("Band", on_delete=models.CASCADE)
    date_released = models.DateField(blank=True, null=True, verbose_name="Date de sortie")
    date_listened = models.DateField(blank=True, null=True, verbose_name="Date d'écoute")
    date_added = models.DateField(auto_now=True, verbose_name="Date d'ajout")
    type_vocal = models.CharField(max_length=2, choices=VOICE_STYLE_CHOICES, null=True, verbose_name="Voix")
    type_album = models.CharField(max_length=2, choices=ALBUM_TYPE_CHOICES, verbose_name="Type")
    type_owned = models.CharField(max_length=2, choices=TYPE_OWNED_CHOICES, verbose_name="Type possédé", blank=True)
    genre_primary = models.ManyToManyField(Genre, related_name="primary_genre", verbose_name="Genre Primaire")
    genre_secondary = models.ManyToManyField(Genre,related_name="secondary_genre", verbose_name="Genre Secondaire", blank=True)
    owned = models.BooleanField(default=False, verbose_name="Possédé")
    rating = models.FloatField(blank=True, null=True, verbose_name="Note")
    thumbnail = models.ImageField(blank=True, upload_to='albums')

    class Meta:
        verbose_name = "Album"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('library:home')


class Playlist(models.Model):

    PLAYLIST_TYPE_CHOICES = [
        ("G", "Genre"),
        ("Y", "Année"),
        ("T", "Top 10"),
        ("F", "5 Étoiles")
    ]

    name = models.CharField(max_length=50, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=50)
    type = models.CharField(max_length=2, choices=PLAYLIST_TYPE_CHOICES)
    optional = models.BooleanField(default=False, verbose_name="Optionel")

    class Meta:
        verbose_name = "Playlist"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Track(models.Model):
    title = models.CharField(max_length=50, verbose_name="Titre")
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    playlist = models.ManyToManyField(Playlist, related_name="playlist", blank=True)
    number = models.IntegerField(verbose_name="Numéro")
    featuring_artist = models.CharField(max_length=50, verbose_name="featuring", blank=True, null=True)
    duration = models.DurationField(verbose_name="durée")
    favorite = models.BooleanField(blank=True, default=False, verbose_name="favori")
    date_added = models.DateField(auto_now=True)
    rating = models.DecimalField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Note",
        max_digits=2,
        decimal_places=1
    )

    class Meta:
        verbose_name = "Morceau"
        ordering = ["number"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('library:home')



