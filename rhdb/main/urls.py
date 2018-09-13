from django.urls import path
from .views import (record_list, RecordDetail, ListRelatedImages,
                   PageDetail, base_view, herbarium_view)



urlpatterns = [
    path('', base_view, name='base-view'),
    path('rec_list/', record_list, name='record-list'),
    path('record/<int:pk>', RecordDetail.as_view(), name='record-info'),
    path('images/<int:pk>', ListRelatedImages.as_view(), name='list-images'),
    path('page/<int:pk>', PageDetail.as_view(), name='page-info'),
    path('herbarium/', herbarium_view),
]