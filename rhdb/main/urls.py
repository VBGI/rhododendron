from django.urls import path
from .views import record_list, SpeciesDetail, RecordDetail


urlpatterns = [
    path('record_list/', record_list, name='record-list'),
    path('species/<int:pk>', SpeciesDetail.as_view(), name='species-info'),
    path('record/<int:pk>', RecordDetail.as_view(), name='record-info'),
]