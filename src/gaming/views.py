from django.views.generic import ListView, DetailView
from .models import Game, PlaySession

import datetime

class GameDashboardView(ListView):
    model = Game
    template_name = 'gaming/dashboard.html'
    context_object_name = 'games'

    def get_queryset(self):
        # On récupère les jeux avec leurs tags pour éviter les requêtes en boucle
        return Game.objects.prefetch_related('tags').all().order_by('-purchase_date')

class GameListView(ListView):
    model = Game
    template_name = 'gaming/game_list.html'
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        current_year = today.year
        games = Game.objects.all().order_by('-purchase_date')

        context['nb_played_games_current_year'] = PlaySession.objects.filter(end_date__year=current_year).count()
        context['rated_games'] = games.filter(rating__gt=0).count()
        context['unrated_games'] = games.filter(rating__isnull=True).count()
        context['last_added'] = Game.objects.all().order_by('-add_date')[0:5]
        context['last_played_games_current_year'] = PlaySession.objects.all().order_by('-end_date')[0:5]

        return context

class GameDetailView(DetailView):
    model = Game
    template_name = 'gaming/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context