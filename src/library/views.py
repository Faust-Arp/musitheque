from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import UserPassesTestMixin

import api
import datetime
from library.forms import AlbumForm, SearchForm, TracksCreateForm, TracksEditForm
from library.models import Band, Album, Track, Playlist


class BandList(ListView):
    model = Band
    context_object_name = "bands"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_added = Band.objects.all().order_by('-date_added')[0:5]

        user = self.request.user
        context['user'] = user
        context['form'] = SearchForm()
        context['last_added'] = last_added
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
        context['albums'] = Album.objects.filter(groupe=band.id, type_album="LP").order_by("date_released")
        context['eps'] = Album.objects.filter(groupe=band.id, type_album="EP").order_by("date_released")
        context['lives'] = Album.objects.filter(groupe=band.id, type_album="LI").order_by("date_released")
        context['singles'] = Album.objects.filter(groupe=band.id, type_album="SI").order_by("date_released")
        context['compiles'] = Album.objects.filter(groupe=band.id, type_album="CO").order_by("date_released")
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
        today = datetime.date.today()
        current_month = today.month
        current_year = today.year
        albums = Album.objects.all()
        five_stars_albums = Album.objects.filter(rating=4.5, type_album='LP').order_by('-date_listened')[0:5]
        rated_count = Album.objects.filter(rating__gt=0).count
        unrated_count = Album.objects.filter(rating=0).count
        listened_current_month = Album.objects.filter(date_listened__year=current_year, date_listened__month=current_month).count
        last_added = Album.objects.all().order_by('-date_added')[0:5]
        last_rated = Album.objects.all().order_by('-date_rated')[0:5]
        user = self.request.user
        context = {
            'user': user,
            'form': SearchForm(),
            'last_added': last_added,
            'last_rated': last_rated,
            'five_stars_albums': five_stars_albums,
            'listened_current_month': listened_current_month,
            'rated_count': rated_count,
            'unrated_count' : unrated_count,
            'albums': albums,
        }
        return context

class AlbumCreate(UserPassesTestMixin, CreateView):
    model = Album
    template_name = "library/album_create.html"
    form_class = AlbumForm

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

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        groupe = form.cleaned_data.get('groupe')
        released = form.cleaned_data.get('date_released')
        listened = form.cleaned_data.get('date_listened')
        thumb = form.cleaned_data.get('thumbnail')

        if Album.objects.filter(title=title, groupe=groupe).exists():
            form.add_error(None, "L'album existe déjà")
            return self.form_invalid(form)
        elif listened is not None and released > listened:
            form.add_error(None, "Vous ne pouvez pas avoir écouté un album avant sa sortie")
            return self.form_invalid(form)
        elif not thumb:
            form.add_error(None, "Une image de la couverture est obligatoire.")
            return self.form_invalid(form)
        else:
            form.save()
            return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class AlbumEdit(UserPassesTestMixin, UpdateView):
    model = Album
    template_name = "library/album_edit.html"
    form_class = AlbumForm

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
        average = api.get_album_average(album.id)
        context['tracks'] = Track.objects.filter(album=album.id).order_by("disc", "number")
        context['full_duration'] = full_duration
        context['average']= average
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Album.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Album.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        album = Album.objects.get(pk=self.kwargs.get('pk'))
        track_count = album.tracks_number

        TracksCreateFormSet = inlineformset_factory(
            Album,
            Track,
            form=TracksCreateForm,
            extra=track_count,
            can_delete=False
        )

        formset = TracksCreateFormSet(self.request.POST or None, instance=album)

        # Prefill the number field based on the index
        for i, form in enumerate(formset.forms):
            if not form.instance.pk:  # Only set for new forms
                form.initial['number'] = i + 1  # Track numbers starting at 1

        return formset

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

class TrackEdit(UserPassesTestMixin, SingleObjectMixin, FormView):
    model = Track
    template_name = "library/track_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Album.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Album.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        album = Album.objects.get(pk=self.kwargs.get('pk'))

        TracksEditFormSet = inlineformset_factory(
            Album,
            Track,
            form=TracksEditForm,
            extra=0
        )

        return TracksEditFormSet(self.request.POST or None, instance=album)

    def form_valid(self, form):
        instances = form.save()

        # On récupère toutes les playlists affectées
        updated_playlists = set()
        for track in instances:
            for playlist in track.playlist.all():
                updated_playlists.add(playlist)

        # On met à jour la date pour chaque playlist concernée
        for playlist in updated_playlists:
            playlist.last_updated = datetime.date.today()
            playlist.save(update_fields=["last_updated"])

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
        tracks = Track.objects.filter(playlist__id=playlist.pk)
        number_of_tracks = tracks.count()
        full_duration = api.get_playlist_duration(playlist.pk)
        number_of_albums = tracks.values_list('album', flat=True).distinct().count()
        context['tracks'] = tracks.order_by("title")
        context['full_duration'] = full_duration
        context['number_of_tracks'] = number_of_tracks
        context['number_of_albums'] = number_of_albums
        return context

def searchview(request):

    if request.method == 'POST':  # If the form has been submitted...
        form = SearchForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            name = form['name'].value()

            bands = Band.objects.filter(name__icontains=name)
            albums = Album.objects.filter(title__icontains=name)

            return render(request, "library/search.html", context={"bands": bands,
                                                                   "albums": albums,
                                                                   })
    else:

        return redirect("bands-list")
