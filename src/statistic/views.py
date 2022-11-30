from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from library.models import Band, Album, Track
from statistic.filters import AlbumFilter, BandFilter
import api


class StatsBandView(ListView):
    model = Band
    queryset = Band.objects.all()
    template_name = "statistic/band.html"
    context_object_name = "bands"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BandFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        countries, bands_number = api.get_band_count_by_country()
        context['countries'] = countries
        context['bands_number'] = bands_number
        context['form'] = self.filterset.form
        return context


class StatsAlbumView(ListView):
    model = Album
    queryset = Album.objects.all()
    template_name = "statistic/album.html"
    context_object_name = "albums"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AlbumFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years, albums_year = api.get_album_by_released_year()
        decades, albums_decade = api.get_album_by_released_decade()
        genres, albums_genres = api.get_album_by_primary_genre()
        families, albums_families = api.get_album_by_family()
        context['years'] = years
        context['decades'] = decades
        context['albums_year'] = albums_year
        context['albums_decade'] = albums_decade
        context['genres'] = genres
        context['albums_genres'] = albums_genres
        context['families'] = families
        context['albums_families'] = albums_families
        context['form'] = self.filterset.form
        return context
