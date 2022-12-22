from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from library.models import Band, Album, Track
from statistic.filters import AlbumFilter, BandFilter
import api


class BandByCountriesView(ListView):
    model = Band
    queryset = Band.objects.all()
    template_name = "statistic/band_by_countries.html"
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


class AlbumByYearsView(ListView):
    model = Album
    queryset = Album.objects.all()
    template_name = "statistic/album_by_years.html"
    context_object_name = "albums"

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = AlbumFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        years, albums_year = api.get_album_by_released_year()
        context['years'] = years
        context['albums_year'] = albums_year

        context['form'] = self.filterset.form
        return context


class AlbumByDecadesView(ListView):
    model = Album
    queryset = Album.objects.all()
    template_name = "statistic/album_by_decades.html"
    context_object_name = "albums"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AlbumFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        decades, albums_decade = api.get_album_by_released_decade()
        context['decades'] = decades
        context['albums_decade'] = albums_decade

        context['form'] = self.filterset.form
        return context


class AlbumByFamiliesView(ListView):
    model = Album
    queryset = Album.objects.all()
    template_name = "statistic/album_by_families.html"
    context_object_name = "albums"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AlbumFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        families, albums_families = api.get_album_by_family()
        context['families'] = families
        context['albums_families'] = albums_families
        print(families)

        context['form'] = self.filterset.form
        return context


class AlbumByGenresView(ListView):
    model = Album
    queryset = Album.objects.all()
    template_name = "statistic/album_by_genres.html"
    context_object_name = "albums"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AlbumFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = self.kwargs.get('family')
        print(family)
        context['family'] = family

        genres_family, albums_genre = api.get_album_by_family_genres(family)
        context['genres_family'] = genres_family
        context['albums_genre'] = albums_genre

        context['form'] = self.filterset.form
        return context

