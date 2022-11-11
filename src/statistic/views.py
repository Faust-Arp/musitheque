from django.shortcuts import render
from django.views.generic import TemplateView

from library.models import Band, Album, Track
import api


class StatsBandView(TemplateView):
    model = Band
    template_name = "statistic/band.html"
    context_object_name = "bands"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        countries, bands_number = api.get_band_count_by_country()
        context['countries'] = countries
        context['bands_number'] = bands_number
        return context


class StatsAlbumView(TemplateView):
    model = Album
    template_name = "statistic/album.html"
    context_object_name = "albums"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years, albums_year = api.get_album_by_released_year()
        decades, albums_decade = api.get_album_by_released_decade()
        genres, albums_genres = api.get_album_by_primary_genre()
        context['years'] = years
        context['decades'] = decades
        context['albums_year'] = albums_year
        context['albums_decade'] = albums_decade
        context['genres'] = genres
        context['albums_genres'] = albums_genres
        return context
