from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from library.forms import TracksCreateForm, TracksCreateFormSet
from library.models import Band, Album, Track
from api import get_album_duration


class LibraryHome(ListView):
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

    def test_func(self):
        return self.request.user.is_admin


class BandDetail(DetailView):
    model = Band

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        band = Band.objects.get(slug=self.kwargs.get('slug'))
        context['albums'] = Album.objects.filter(groupe=band.id).order_by("date_released")
        return context


class BandDelete(UserPassesTestMixin, DeleteView):
    model = Band
    success_url = reverse_lazy("library:home")
    context_object_name = "band"

    def test_func(self):
        return self.request.user.is_admin


class AlbumCreate(UserPassesTestMixin, CreateView):
    model = Album
    template_name = "library/album_create.html"
    fields = [
        "title",
        "groupe",
        "date_released",
        "date_listened",
        "type_vocal",
        "type_album",
        "owned",
        "type_owned",
        "genre_primary",
        "genre_secondary",
        "rating",
        "thumbnail",
    ]

    # Cette fonction sert à ajouter le widget DatePicker sur les champs date du formulaire
    def get_form(self, form_class=None):
        form = super(AlbumCreate, self).get_form(form_class)
        form.fields['date_released'].widget = AdminDateWidget(attrs={'type': 'date'})
        form.fields['date_listened'].widget = AdminDateWidget(attrs={'type': 'date'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button_value'] = "Créer"
        return context

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

    def test_func(self):
        return self.request.user.is_admin


class AlbumDetail(DetailView):
    model = Album
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = Album.objects.get(pk=self.kwargs.get('pk'))
        full_duration = get_album_duration(album.id)
        context['tracks'] = Track.objects.filter(album=album.id).order_by("number")
        context['full_duration'] = full_duration
        return context


class AlbumDelete(UserPassesTestMixin, DeleteView):
    model = Album
    success_url = reverse_lazy("library:home")
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

    def get_success_url(self):
        return reverse('library:home')

    def test_func(self):
        return self.request.user.is_admin

