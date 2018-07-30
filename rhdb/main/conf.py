from django.conf import settings
from appconf import AppConf


class RhododendronAppConf(AppConf):

    PAGINATION_SIZE = 30

    class Meta:
        prefix = 'rhd'
