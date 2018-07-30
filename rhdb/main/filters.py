import django_filters

from .models import Record

class RecordFilter(django_filters.FilterSet):
    class Meta:
        model = Record
        fields = {
                 'species__name': ['icontains'],
                 'region': ['icontains'],
                 'district': ['icontains'],
                 'latitude': ['lt', 'gt'],
                 'longitude': ['lt', 'gt'],
                 'content': ['icontains']
                  }

