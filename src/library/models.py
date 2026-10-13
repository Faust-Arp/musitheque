from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Band(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    country = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)
    thumbnail = models.ImageField(blank=True, upload_to='bands')

    class Meta:
        verbose_name = "Artiste"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


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
        ("CO", "Compilation"),
        ("ST", "Original Soundtrack")
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
    discovery_source = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Origine de la découverte",
    )
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
    sclist_creation_date = models.DateField(blank=True, null=True, verbose_name="Date de création liste senscritique")

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


class RatingHistory(models.Model):
    album = models.ForeignKey("Album", on_delete=models.CASCADE, related_name="rating_history")
    old_rating = models.FloatField(blank=True, null=True, verbose_name="Old Rating")
    new_rating = models.FloatField(blank=True, null=True, verbose_name="New Rating")
    date_changed = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-date_changed"]


class ScListFollowUp(models.Model):
    playlist = models.ForeignKey("Playlist", on_delete=models.CASCADE, related_name="sc_list_follow_up")
    old_views_number = models.IntegerField(default=0, blank=True, null=True)
    new_views_number = models.IntegerField(default=0, blank=True, null=True)
    old_likes_number = models.IntegerField(default=0, blank=True, null=True)
    new_likes_number = models.IntegerField(default=0, blank=True, null=True)
    old_albums_number = models.IntegerField(default=0, blank=True, null=True)
    new_albums_number = models.IntegerField(default=0, blank=True, null=True)
    date_changed = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-date_changed"]


class ListeningLog(models.Model):
    playlist = models.ForeignKey("Playlist", on_delete=models.CASCADE, related_name="listening_log")
    start_date = models.DateField(verbose_name="Début de la période")
    end_date = models.DateField(verbose_name="Fin de la période", null=True, blank=True)
    nb_of_songs = models.IntegerField(verbose_name="Nombre de morceaux")
    class Meta:
        ordering = ["-start_date"]