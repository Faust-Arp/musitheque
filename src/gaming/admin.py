from django.contrib import admin
from .models import Game, GameTag, PlaySession, Dlc


# Cela permet d'ajouter des sessions directement depuis la fiche d'un jeu
class PlaySessionInline(admin.TabularInline):
    model = PlaySession
    extra = 1  # Affiche une ligne vide par défaut pour ajouter une session rapidement

class DlcInline(admin.StackedInline):
    model = Dlc
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    # Les colonnes affichées dans la liste des jeux
    list_display = ('title', 'purchase_date', 'price', 'rating')

    # Filtres sur le côté droit
    list_filter = ('tags', 'rating', 'purchase_date')

    # Barre de recherche
    search_fields = ('title', 'comment')

    # Organisation de la fiche détaillée
    fieldsets = (
        ('Infos de base', {
            'fields': ('title', 'steam_id','developper', 'editor', 'tags', 'release_date', 'cover_image')
        }),
        ('Achat', {
            'fields': ('price', 'purchase_date')
        }),
        ('Évaluation & Succès', {
            'fields': ('rating', 'comment', 'total_achievements', 'unlocked_achievements')
        }),
    )

    inlines = [PlaySessionInline, DlcInline]

@admin.register(Dlc)
class DlcAdmin(admin.ModelAdmin):
    # Les colonnes affichées dans la liste des jeux
    list_display = ('title', 'purchase_date', 'price', 'rating')

    # Filtres sur le côté droit
    list_filter = ('tags', 'rating', 'purchase_date')

    # Barre de recherche
    search_fields = ('title', 'comment')

    # Organisation de la fiche détaillée
    fieldsets = (
        ('Infos de base', {
            'fields': ('game', 'title', 'steam_id', 'tags', 'release_date', 'cover_image')
        }),
        ('Achat', {
            'fields': ('price', 'purchase_date')
        }),
        ('Évaluation & Succès', {
            'fields': ('rating', 'comment')
        }),
    )

@admin.register(GameTag)
class GameTagAdmin(admin.ModelAdmin):
    search_fields = ('name',)


# On peut aussi garder l'accès direct aux sessions si besoin
@admin.register(PlaySession)
class PlaySessionAdmin(admin.ModelAdmin):
    list_display = ('game', 'start_date', 'end_date', 'time_played')
    list_filter = ('game', 'start_date')