from django.contrib import admin

from library.models import Band, Genre, Album, Track, Playlist, ScListFollowUp, ListeningLog


class TrackInline(admin.StackedInline):
    model = Track
    extra = 1

    # Organisation de la fiche détaillée
    fieldsets = (
        ('Infos de base', {
            'fields': ('album', 'disc', 'number','title', 'duration', 'type')
        }),
        ('Classification', {
            'fields': ('rating', 'playlist', 'favorite')
        }),
    )

class ListeningLogInline(admin.StackedInline):
    model = ListeningLog
    extra = 1

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):

    # Les colonnes affichées dans la liste des artistes
    list_display = ("name", "country", "active")

    # Filtres sur le côté droit
    list_filter = ('name', 'country', 'active')

    # Barre de recherche
    search_fields = ['name']

    # Organisation de la fiche détaillée
    fieldsets = (
        ('Infos de base', {
            'fields': ('name', 'country')
        }),
        ('Autres', {
            'fields': ('active', 'thumbnail')
        })
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    # Les colonnes affichées dans la liste des genres
    list_display = ("name", "family")

    # Filtres sur le côté droit
    list_filter = ("name", "family")

    # Barre de recherche
    search_fields = ['name']

    # Organisation de la fiche détaillée
    fields = ("name", "family")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):

    # Les colonnes affichées dans la liste des playlists
    list_display = ("name", "date_added", "sclist_creation_date")

    # Filtres sur le côté droit
    list_filter = ("name", "type")

    # Barre de recherche
    search_fields = ['name']

    # Organisation de la fiche détaillée
    fields = ('name', 'type','color', 'optional', 'sclist_creation_date', 'thumbnail')

    inlines = [ListeningLogInline]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):

    # Les colonnes affichées dans la liste des albums
    list_display = ('groupe', "title", "date_released", "rating", 'tracks_number')

    # Filtres sur le côté droit
    list_filter = ("type_album", "type_owned", "rating")

    # Barre de recherche
    search_fields = ['title']

    # Organisation de la fiche détaillée
    fieldsets = (
        ('Infos de base', {
            'fields': ('groupe', 'title','number_album', 'tracks_number', 'type_album', 'thumbnail')
        }),
        ('Dates', {
            'fields': ('date_released', 'date_listened', 'date_rated')
        }),
        ('Catégorisation & Note', {
            'fields': ('type_owned', 'genre_primary', 'rating', 'comment')
        }),
    )

    inlines = [TrackInline]

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):

    # Les colonnes affichées dans la liste des albums
    list_display = ("album", "number", "title", "duration", "rating")

    # Filtres sur le côté droit
    list_filter = ("rating", "type")

    # Barre de recherche
    search_fields = ['title']

    # Organisation de la fiche détaillée
    fieldsets = (
        ('Infos de base', {
            'fields': ('album', 'disc', 'number','title', 'duration', 'type')
        }),
        ('Classification', {
            'fields': ('rating', 'playlist', 'favorite')
        }),
    )


