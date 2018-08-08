from django.urls import path
from .views import (record_list, RecordDetail, ListRelatedImages,
                   PageDetail)


urlpatterns = [
    path('record_list/', record_list, name='record-list'),
    path('record/<int:pk>', RecordDetail.as_view(), name='record-info'),
    path('images/<int:pk>', ListRelatedImages.as_view(), name='list-images'),
    path('page/<int:pk>', PageDetail.as_view(), name='page-info')
]