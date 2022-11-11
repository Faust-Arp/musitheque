from django.urls import path
from statistic.views import StatsBandView, StatsAlbumView

app_name = "statistic"

urlpatterns = [
    path('band/', StatsBandView.as_view(), name='stats-band'),
    path('album/', StatsAlbumView.as_view(), name='stats-album'),
]