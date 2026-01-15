from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Band(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)
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

    # def get_absolute_url(self):
    #     return reverse('library:bands-list')


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50)
    family = models.CharField(max_length=50, blank=True)

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
        ("EP", "EP"),
        ("LI", "Live"),
        ("SI", "Single"),
        ("CO", "Compilation")
    ]

    TYPE_OWNED_CHOICES = [
        ("AC", "Acheté"),
        ("TL", "Téléchargé"),
    ]

    title = models.CharField(max_length=100, verbose_name="titre")
    slug = models.SlugField(max_length=100, blank=True)
    groupe = models.ForeignKey("Band", on_delete=models.CASCADE)
    date_released = models.DateField(blank=True, null=True, verbose_name="Date de sortie")
    date_listened = models.DateField(blank=True, null=True, verbose_name="Date d'écoute")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    date_rated = models.DateTimeField(blank=True, null=True, verbose_name="Date de notation")
    tracks_number = models.IntegerField(verbose_name="Nombre de morceaux")
    type_album = models.CharField(max_length=2, choices=ALBUM_TYPE_CHOICES, verbose_name="Type")
    type_owned = models.CharField(max_length=2, choices=TYPE_OWNED_CHOICES, verbose_name="Type possédé", blank=True)
    genre_primary = models.ManyToManyField(Genre, related_name="primary_genre", verbose_name="Genre Primaire")
    number_album = models.PositiveSmallIntegerField(default=1, verbose_name="Nombre d'albums")
    rating = models.FloatField(blank=True, null=True, verbose_name="Note")
    comment = models.TextField(
        blank=True,
        verbose_name="Commentaire",
        help_text="Avis personnel sur l'album"
    )
    thumbnail = models.ImageField(blank=True, upload_to='albums')

    class Meta:
        verbose_name = "Album"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


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
    color = models.CharField(max_length=7, verbose_name="Couleur", blank=True)
    optional = models.BooleanField(default=False, verbose_name="Optionel")
    date_added = models.DateField(auto_now=True, blank=True, null=True, verbose_name="Ajoutée")
    last_updated = models.DateField(blank=True, null=True, verbose_name="Modifiée")
    like = models.IntegerField(default=0, blank=True, null=True)
    fan = models.IntegerField(default=0, blank=True, null=True)
    thumbnail = models.ImageField(blank=True, upload_to='playlists')

    class Meta:
        verbose_name = "Playlist"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_album_thumbnails(self):
        album_ids = self.playlist.all().values_list('album', flat=True).distinct()[:4]
        return Album.objects.filter(id__in=album_ids).only('thumbnail')


class Track(models.Model):

    TRACK_TYPE_CHOICES = [
        ("IT", "Interlude"),
        ("RG", "Régulière")
    ]

    title = models.CharField(max_length=150, verbose_name="Titre")
    slug = models.SlugField(max_length=150, blank=True)
    type = models.CharField(max_length=2, choices=TRACK_TYPE_CHOICES, verbose_name="Type")
    album = models.ForeignKey("Album", on_delete=models.CASCADE)
    disc = models.IntegerField(verbose_name="CD", default=1)
    playlist = models.ManyToManyField(Playlist, related_name="playlist", blank=True)
    number = models.IntegerField(verbose_name="Numéro")
    featuring_artist = models.CharField(max_length=50, verbose_name="featuring", blank=True, null=True)
    duration = models.DurationField(verbose_name="durée")
    favorite = models.BooleanField(blank=True, default=False, verbose_name="favori")
    date_added = models.DateField(auto_now=True)
    rating = models.FloatField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Note",
    )

    class Meta:
        verbose_name = "Morceau"
        ordering = ["disc", "number"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)



