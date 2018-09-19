from django.urls import path
from .views import (record_list, RecordDetail, ListRelatedImages,
                   PageDetail, base_view, herbarium_view, AlbumView)
from .conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', base_view, name='base-view'),
    path('rec_list/', record_list, name='record-list'),
    path('record/<int:pk>', RecordDetail.as_view(), name='record-info'),
    path('images/<int:pk>', ListRelatedImages.as_view(), name='list-images'),
    path('page/<int:pk>', PageDetail.as_view(), name='page-info'),
    path('herbarium/', herbarium_view, name='herb-data'),
    path(settings.RHD_ALBUM_URL + '<slug:slug>', AlbumView.as_view(),
         name='show-album')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)