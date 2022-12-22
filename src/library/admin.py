from django.contrib import admin

from library.models import Band, Genre, Album, Track, Playlist


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "region",
        "city",
        "active",
        "date_added",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "family",
    )


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "color",
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "date_released",
        "owned",
        "rating",
        "number_album",
    )


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "duration",
        "favorite",
        "rating",
    )


