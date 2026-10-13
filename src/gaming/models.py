from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class GameTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=255)
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    developper = models.CharField(max_length=100, blank=True, null=True)
    editor = models.CharField(max_length=100, blank=True, null=True)
    add_date = models.DateField(auto_now_add=True, verbose_name="Date d'ajout")
    release_date = models.DateField(null=True, blank=True, verbose_name="Date de sortie officielle")
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name="Jaquette")

    # Infos d'achat
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Prix d'achat")
    purchase_date = models.DateField(default=timezone.now, verbose_name="Date d'achat")

    # Évaluation
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Note de 1 à 10",
        null=True, blank=True
    )
    comment = models.TextField(verbose_name="Mon avis", blank=True)

    # Succès
    total_achievements = models.PositiveIntegerField(default=0)
    unlocked_achievements = models.PositiveIntegerField(default=0)

    # Catégorisation
    tags = models.ManyToManyField(GameTag, blank=True)

    def __str__(self):
        return self.title

class Dlc(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    add_date = models.DateField(auto_now_add=True, verbose_name="Date d'ajout")
    release_date = models.DateField(null=True, blank=True, verbose_name="Date de sortie officielle")
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name="Jaquette")

    #Infos d'achat
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Prix d'achat")
    purchase_date = models.DateField(default=timezone.now, verbose_name="Date d'achat")

    # Évaluation
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Note de 1 à 10",
        null=True, blank=True
    )
    comment = models.TextField(verbose_name="Mon avis", blank=True)

    # Catégorisation
    tags = models.ManyToManyField(GameTag, blank=True)

class PlaySession(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    start_date = models.DateField(verbose_name="Début de la période")
    end_date = models.DateField(verbose_name="Fin de la période", null=True, blank=True)
    time_played = models.PositiveIntegerField(default=0, verbose_name="Temps de jeu")
    summary = models.TextField(blank=True, help_text="Qu'as-tu fait / pensé durant cette période ?")

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        if self.end_date:
            return f"Session {self.game.title} du {self.start_date} au {self.end_date}"
        return f"Session {self.game.title} (En cours depuis le {self.start_date})"