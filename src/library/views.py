from django.contrib import messages
from django.db.models import Subquery, OuterRef, F, Max
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
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
from django.utils import timezone
from library.forms import AlbumForm, SearchForm, TracksCreateForm, TracksEditForm, PlaylistFollowUpForm, PlaylistListeningLogForm
from library.models import Band, Album, Track, Playlist, ScListFollowUp, RatingHistory, ListeningLog
from gaming.models import Game


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
        # On récupère le contexte de base
        context = super().get_context_data(**kwargs)
        # L'objet Band est déjà disponible dans self.object grâce à DetailView
        band = self.object

        # On définit les types pour automatiser la création du contexte
        types = {
            'albums': 'LP',
            'eps': 'EP',
            'lives': 'LI',
            'singles': 'SI',
            'compiles': 'CO',
            'soundtracks': 'ST'
        }

        # On boucle pour éviter la répétition de code
        for context_key, type_code in types.items():
            context[context_key] = band.album_set.filter(
                type_album=type_code
            ).order_by("date_released")

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
        listened_current_month = Album.objects.filter(date_listened__year=current_year, date_listened__month=current_month).exclude(type_album='SI').count()
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

    def form_valid(self, form, **kwargs):
        album = self.get_object()  # Plus simple que Album.objects.get(pk=...)
        old_rating = album.rating
        new_rating = form.cleaned_data.get('rating')

        if old_rating == 0 and new_rating == 0:
            # Pas de changement, on sauvegarde et on quitte
            return super().form_valid(form)

        if old_rating == 0 and new_rating > 0:
            album.rating_date = datetime.date.today() # Hypothèse : tu voulais mettre à jour une date ?
            # Note : Si 'rating' est un champ du formulaire, form.save() l'écrasera
            # Il vaut mieux modifier l'instance avant le save.
            album.save()
            return super().form_valid(form)

        if old_rating != new_rating:
            RatingHistory.objects.create(
                album=album,
                old_rating=old_rating,
                new_rating=new_rating
            )
            return super().form_valid(form)

        # CAS MANQUANT : Si old_rating == new_rating
        # On doit quand même retourner quelque chose !
        return super().form_valid(form)


class AlbumDetail(DetailView):
    model = Album
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = Album.objects.get(pk=self.kwargs.get('pk'))
        band = Band.objects.get(name=album.groupe)
        full_duration = api.get_album_duration(album.id)
        average = api.get_album_average(album.id)
        rating_history = RatingHistory.objects.filter(album=album)
        context['tracks'] = Track.objects.filter(album=album.id).order_by("disc", "number")
        context['full_duration'] = full_duration
        context['average']= average
        context['band'] = band
        context['rating_history'] = rating_history
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

        context['nb_of_genre_playlists'] = Playlist.objects.filter(type='G').count()
        context['nb_of_year_playlists'] = Playlist.objects.filter(type='Y').count()

        # ÉTAPE 1 : Trouver la date MAX pour chaque playlist
        last_dates = ScListFollowUp.objects.values('playlist').annotate(
            last_date=Max('date_changed')
        )

        playlist_ids_with_followup = [item['playlist'] for item in last_dates]
        date_map = {item['playlist']: item['last_date'] for item in last_dates}

        # ÉTAPE 2 : Récupérer les objets de suivi correspondants
        latest_followups = ScListFollowUp.objects.filter(
            playlist_id__in=playlist_ids_with_followup,
            date_changed__in=date_map.values()
        )

        followup_map = {fu.playlist_id: fu for fu in latest_followups}

        # ÉTAPE 3 : Récupérer les playlists
        playlists = Playlist.objects.filter(type='G')

        stats_list = []
        for p in playlists:
            if p.id not in followup_map:
                continue

            # Calcul du nombre d'albums réels dans la playlist
            tracks = Track.objects.filter(playlist__id=p.pk)
            # Assure-toi que 'album' est bien le nom du champ ForeignKey dans ton modèle Track
            number_of_albums = tracks.values_list('album', flat=True).distinct().count()

            fu = followup_map[p.id]

            new_v = fu.new_views_number or 0
            old_v = fu.old_views_number or 0
            growth = new_v - old_v

            fu_albums = fu.new_albums_number or 0

            # --- CORRECTION ICI ---
            # On groupe les conditions de performance entre parenthèses
            # ET on exige que le nombre d'albums soit différent
            if (new_v > 0 or growth > 0) and (fu_albums != number_of_albums):
                # Calcul de la différence pour l'affichage (optionnel)
                album_diff = number_of_albums - fu_albums

                stats_list.append({
                    'playlist': p,
                    'views_growth': growth,
                    'total_views': new_v,
                    'total_likes': fu.new_likes_number or 0,
                    'current_albums': number_of_albums,  # Le vrai nombre actuel
                    'recorded_albums': fu_albums,  # Le nombre enregistré dans le suivi
                    'album_diff': album_diff  # La différence (ex: +3)
                })

        # Tri par croissance décroissante
        stats_list.sort(key=lambda x: x['views_growth'], reverse=True)

        context['top_growing_playlists'] = stats_list[:5]

        return context

class PlaylistDetail(DetailView):
    model = Playlist
    context_object_name = "playlist"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # On utilise self.object qui est déjà chargé par la DetailView
        playlist = self.object

        tracks = Track.objects.filter(playlist__id=playlist.pk)

        # Statistiques de suivi SensCritique (dernier an maximum, ordre chronologique)
        one_year_ago = timezone.now() - datetime.timedelta(days=365)
        followups = list(playlist.sc_list_follow_up.filter(date_changed__gte=one_year_ago).order_by('date_changed'))

        sc_labels = [f.date_changed.strftime("%d/%m/%Y") for f in followups]
        sc_views = [f.new_views_number or 0 for f in followups]
        sc_likes = [f.new_likes_number or 0 for f in followups]
        sc_albums = [f.new_albums_number or 0 for f in followups]

        number_of_albums = tracks.values_list('album', flat=True).distinct().count()

        context['tracks'] = tracks.order_by("title")
        context['full_duration'] = api.get_playlist_duration(playlist.pk)
        context['number_of_tracks'] = tracks.count()
        context['number_of_albums'] = number_of_albums
        context['sc_labels'] = sc_labels
        context['sc_views'] = sc_views
        context['sc_likes'] = sc_likes
        context['sc_albums'] = sc_albums
        context['has_sc_data'] = len(followups) > 0
        context['sclist_creation-date'] = playlist.sclist_creation_date
        context['listening_logs'] = playlist.listening_log.all()
        return context

class PlaylistFollowUpCreateView(UserPassesTestMixin, CreateView):
    model = ScListFollowUp
    form_class = PlaylistFollowUpForm
    template_name = "library/PlaylistFollowUp.html"

    def form_valid(self, form):
        # 1. On récupère la playlist grâce à l'ID dans l'URL (pk)
        playlist = Playlist.objects.get(pk=self.kwargs.get('pk'))
        form.instance.playlist = playlist

        # 2. On récupère le dernier suivi pour peupler les "old_..."
        last_followup = playlist.sc_list_follow_up.first()
        if last_followup:
            form.instance.old_views_number = last_followup.new_views_number
            form.instance.old_likes_number = last_followup.new_likes_number
            form.instance.old_albums_number = last_followup.new_albums_number

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On ajoute la playlist au contexte pour l'afficher dans le template
        context['playlist'] = Playlist.objects.get(pk=self.kwargs.get('pk'))
        context['submit_button_value'] = "Ajouter le suivi"
        return context

    def get_success_url(self):
        return reverse('library:playlist', kwargs={'pk': self.kwargs.get('pk')})

    def test_func(self):
        # Correction : on utilise généralement is_staff ou is_superuser
        # car is_admin n'est pas un attribut par défaut de User
        return self.request.user.is_staff

class PlaylistLIsteningLogCreateView(UserPassesTestMixin, CreateView):
    model = ListeningLog
    form_class = PlaylistListeningLogForm
    template_name = "library/PlaylistLIsteningLog.html"

    def form_valid(self, form):
        # 1. On récupère la playlist grâce à l'ID dans l'URL (pk)
        playlist = Playlist.objects.get(pk=self.kwargs.get('pk'))
        form.instance.playlist = playlist

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On ajoute la playlist au contexte pour l'afficher dans le template
        context['playlist'] = Playlist.objects.get(pk=self.kwargs.get('pk'))
        context['submit_button_value'] = "Ajouter le suivi"
        return context

    def get_success_url(self):
        return reverse('library:playlist', kwargs={'pk': self.kwargs.get('pk')})

    def test_func(self):
        # Correction : on utilise généralement is_staff ou is_superuser
        # car is_admin n'est pas un attribut par défaut de User
        return self.request.user.is_staff

def searchview(request):

    if request.method == 'POST':  # If the form has been submitted...
        form = SearchForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            name = form['name'].value()

            bands = Band.objects.filter(name__icontains=name)
            albums = Album.objects.filter(title__icontains=name)
            games = Game.objects.filter(title__icontains=name)

            return render(request,
                "library/search.html",
                context={
                    "bands": bands,
                    "albums": albums,
                    "games": games,
                })
    else:

        return redirect("bands-list")
