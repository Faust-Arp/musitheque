from django.urls import path
from .views import GameDashboardView, GameListView, GameDetailView

app_name = 'gaming'

urlpatterns = [
    path('dashboard/', GameDashboardView.as_view(), name='dashboard'),
    path('games', GameListView.as_view(), name='games-list'),
    path('game/<pk>', GameDetailView.as_view(), name='game'),
]