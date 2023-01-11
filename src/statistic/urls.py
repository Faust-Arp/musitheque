from django.urls import path
from statistic.views import BandByCountriesView, AlbumByYearsView, AlbumByDecadesView, AlbumByFamiliesView
from statistic.views import AlbumByGenresView, ListenedReleasedView, AlbumByRating

app_name = "statistic"

urlpatterns = [
    path('band/by_country', BandByCountriesView.as_view(), name='band-by-country'),
    path('album/by_years', AlbumByYearsView.as_view(), name='album-by-years'),
    path('album/by_decades', AlbumByDecadesView.as_view(), name='album-by-decades'),
    path('album/by_families', AlbumByFamiliesView.as_view(), name='album-by-families'),
    path('album/by_genres/<str:family>', AlbumByGenresView.as_view(), name='album-by-genres'),
    path('album/by_rating', AlbumByRating.as_view(), name='album-by-rating'),
    path('album/listened_released', ListenedReleasedView.as_view(), name='listened-released'),
]