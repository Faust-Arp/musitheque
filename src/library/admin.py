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
    )


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date_released",
        "owned",
        "rating",
    )


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "duration",
        "favorite",
        "rating",
    )


