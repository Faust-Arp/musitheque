import django_filters
from django_filters import CharFilter, ModelChoiceFilter, NumberFilter

from library.models import Album, Band


class AlbumFilter(django_filters.FilterSet):
    title = CharFilter(lookup_expr='icontains', label='Titre contenant:')
    groupe__name = CharFilter(lookup_expr='icontains', label='Nom du groupe contenant:')
    date_released = CharFilter(lookup_expr='year', label='Année de sortie:')
    date_listened = CharFilter(lookup_expr='year', label='Année d\'écoute:')
    genre_primary = CharFilter(method='filter_tags', label='Genre principal contenant:')
    rating_lte = NumberFilter(field_name='rating', lookup_expr='lte', label='Note inférieure ou égale à:')
    rating_gte = NumberFilter(field_name='rating', lookup_expr='gte', label='Note supérieure ou égale à:')

    class Meta:
        model = Album
        fields = [
            'title',
            'groupe__name',
            'date_released',
            'date_listened',
            'genre_primary',
            'rating_lte',
            'rating_gte',
        ]

    def filter_tags(self, queryset, name, value):
        return queryset.filter(genre_primary__name__icontains=value)


class BandFilter(django_filters.FilterSet):
    class Meta:
        model = Band
        fields = {
            'name': ['icontains'],
            'country': ['icontains'],
            'region': ['icontains'],
            'city': ['icontains'],
            'active': ['exact']
        }