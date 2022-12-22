from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import api
from library.forms import TracksCreateForm, TracksCreateFormSet, AlbumCreateForm
from library.models import Band, Album, Track, Playlist


class BandList(ListView):
    model = Band
    context_object_name = "bands"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class BandCreate(UserPassesTestMixin, CreateView):
    model = Band
    template_name = "library/band_create.html"
    fields = [
        "name",
        "country",
        "region",
        "city",
        "active",
        "thumbnail",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button_value'] = "Ajouter"
        return context

    def test_func(self):
        return self.request.user.is_admin

    def get_success_url(self):
        return reverse('library:bands-list')


class BandEdit(UserPassesTestMixin, UpdateView):
    model = Band
    template_name = "library/band_create.html"
    fields = [
        "name",
        "country",
        "region",
        "city",
        "active",
        "thumbnail",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button_value'] = "Modifier"
        return context

    def get_success_url(self, **kwargs):
        band_id = self.kwargs.get('pk')
        return reverse('library:band', kwargs={'pk': band_id})

    def test_func(self):
        return self.request.user.is_admin


class BandDetail(DetailView):
    model = Band

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        band = Band.objects.get(pk=self.kwargs.get('pk'))
        album_owned, album_count = api.get_album_owned_count_for_band(band.id)
        context['albums'] = Album.objects.filter(groupe=band.id).order_by("date_released")
        context['album_owned'] = album_owned
        context['album_count'] = album_count
        return context


class BandDelete(UserPassesTestMixin, DeleteView):
    model = Band
    success_url = reverse_lazy("library:bands-list")
    context_object_name = "band"

    def test_func(self):
        return self.request.user.is_admin


class AlbumList(ListView):
    model = Album
    context_object_name = "albums"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class AlbumCreate(UserPassesTestMixin, CreateView):
    model = Album
    template_name = "library/album_create.html"
    form_class = AlbumCreateForm

    def get_initial(self):
        groupe = get_object_or_404(Band, pk=self.kwargs.get('pk'))
        return {
            'groupe': groupe,
        }

    # Cette fonction sert à ajouter le widget DatePicker sur les champs date du formulaire
    def get_form(self, form_class=None):
        form = super(AlbumCreate, self).get_form(form_class)
        form.fields['date_released'].widget = AdminDateWidget(attrs={'type': 'date'})
        form.fields['date_listened'].widget = AdminDateWidget(attrs={'type': 'date'})
        form.fields['groupe'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button_value'] = "Créer"
        return context

    def get_success_url(self):
        band_id = self.kwargs.get('pk')
        return reverse('library:band', kwargs={'pk': band_id})

    def test_func(self):
        return self.request.user.is_admin


class AlbumEdit(UserPassesTestMixin, UpdateView):
    model = Album
    template_name = "library/album_create.html"
    fields = [
        "title",
        "groupe",
        "date_released",
        "date_listened",
        "type_vocal",
        "type_album",
        "type_owned",
        "genre_primary",
        "genre_secondary",
        "owned",
        "rating",
        "thumbnail",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button_value'] = "Modifier"
        return context

    def get_success_url(self, **kwargs):
        album_id = self.kwargs.get('pk')
        return reverse('library:album', kwargs={'pk': album_id})

    def test_func(self):
        return self.request.user.is_admin


class AlbumDetail(DetailView):
    model = Album
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = Album.objects.get(pk=self.kwargs.get('pk'))
        band = Band.objects.get(name=album.groupe)
        full_duration = api.get_album_duration(album.id)
        context['tracks'] = Track.objects.filter(album=album.id).order_by("number")
        context['full_duration'] = full_duration
        context['band'] = band
        return context


class AlbumDelete(UserPassesTestMixin, DeleteView):
    model = Album
    success_url = reverse_lazy("library:albums-list")
    context_object_name = "album"

    def test_func(self):
        return self.request.user.is_admin


class TrackCreate(UserPassesTestMixin, SingleObjectMixin, FormView):
    model = Track
    template_name = "library/track_create.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Album.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Album.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return TracksCreateFormSet(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Les changements ont été sauvegardés."
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        album_id = self.kwargs.get('pk')
        return reverse('library:album', kwargs={'pk': album_id})

    def test_func(self):
        return self.request.user.is_admin


class PlaylistList(ListView):
    model = Playlist
    context_object_name = "playlists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class PlaylistDetail(DetailView):
    model = Playlist
    context_object_name = "playlist"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = Playlist.objects.get(pk=self.kwargs.get('pk'))
        number_of_tracks = Track.objects.filter(playlist__id=playlist.pk).count()
        full_duration = api.get_playlist_duration(playlist.pk)
        context['tracks'] = Track.objects.filter(playlist__id=playlist.pk).order_by("title")
        context['full_duration'] = full_duration
        context['number_of_tracks'] = number_of_tracks
        return context
