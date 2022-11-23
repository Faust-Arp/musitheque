import django_filters
from library.models import Album, Band


class AlbumFilter(django_filters.FilterSet):
    class Meta:
        model = Album
        fields = {
            'title' : ['icontains'],
            'groupe__name': ['icontains'],
            'date_released': ['year'],
            'date_listened': ['year'],
            'rating': ['lte', 'gte'],
            'type_vocal': ['exact'],
        }


class BandFilter(django_filters.FilterSet):
    class Meta:
        model = Band
        fields = {
            'name' : ['icontains'],
            'country' : ['icontains'],
            'region' : ['icontains'],
            'city' : ['icontains'],
            'active' : ['exact']
        }