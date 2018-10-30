from django.conf import settings
from appconf import AppConf


class RhododendronAppConf(AppConf):

    PAGINATION_SIZE = 30
    BGI_HERB_URL = 'http://botsad.ru/hitem/json'
    BGI_HERB_SEARCH_PARAMETERS = 'genus=rhododendron'
    ALBUM_URL = 'jsonalbum/'
    THUMBNAIL_DIR = 'thumbs'
    THUMBNAIL_W = 100
    THUMBNAIL_H = 200
    class Meta:
        prefix = 'rhd'
