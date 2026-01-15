import django_filters
from django.db.models.functions import ExtractMonth, ExtractYear
from django_filters import CharFilter, NumberFilter, BooleanFilter, DateFilter

from library.models import Album, Band


class AlbumFilter(django_filters.FilterSet):
    groupe__name = CharFilter(lookup_expr='icontains', label='Nom du groupe contenant:')
    date_released = CharFilter(lookup_expr='year', label='Année de sortie:')
    month_listened = NumberFilter(method='filter_by_month', label='Mois d\'écoute:')
    year_listened = NumberFilter(method='filter_by_year', label='Année d\'écoute:')
    genre_primary = CharFilter(method='filter_tags', label='Genre principal contenant:')
    rating_lte = NumberFilter(field_name='rating', lookup_expr='lte', label='Note inférieure ou égale à:')
    rating_gte = NumberFilter(field_name='rating', lookup_expr='gte', label='Note supérieure ou égale à:')

    class Meta:
        model = Album
        fields = [
            'groupe__name',
            'date_released',
            'date_listened',
            'date_listened',
            'genre_primary',
            'rating_lte',
            'rating_gte',
        ]


    def filter_tags(self, queryset, name, value):
        return queryset.filter(genre_primary__name__icontains=value)

    def filter_by_month(self, queryset, name, value):
        return queryset.annotate(month_listened=ExtractMonth('date_listened')).filter(month_listened=value)

    def filter_by_year(self, queryset, name, value):
        return queryset.annotate(year_listened=ExtractYear('date_listened')).filter(year_listened=value)


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
