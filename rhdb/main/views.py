from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from .conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from .filters import RecordFilter
from .models import Record, Species, Image, Page
from django.views.generic import DetailView, ListView
import urllib.request




def record_list(request):
    filtered_objects = RecordFilter(request.GET, queryset=Record.objects.all())
    page = request.GET.get('page', 1)
    paginator = Paginator(filtered_objects.qs,
                          getattr(settings, 'RHD_PAGINATION_SIZE', 50))
    try:
        objects = paginator.get_page(page)
    except EmptyPage:
        objects = paginator.get_page(1)
    return render(request, 'record-list.html',
                  {'objects': objects})

def base_view(request):
    return render(request, 'base.html')


def herbarium_view(request):
    if request.is_ajax():
        pars = getattr(settings, 'RHD_BGI_HERB_SEARCH_PARAMETERS', '')
        url = getattr(settings, 'RHD_BGI_HERB_URL', '')
        data = cache.get('herbarium-data')
        if data is None:
            with urllib.request.urlopen(url + '/?' + pars) as response:
               data = response.read()
            cache.set('herbarium-data', data, 3600 * 24)
        return HttpResponse(data, content_type="application/json")
    else:
        return render(request, 'herbarium.html')


class RecordDetail(DetailView):
    model = Record
    template_name = 'record-details.html'

class PageDetail(DetailView):
    model = Page
    template_name = 'page-details.html'


class ListRelatedImages(ListView):
    model = Image
    http_method_names = ['get',]

    def dispatch(self, request, *args, **kwargs):
        self.record_pk = self.kwargs.get('pk', -1)
        try:
            Record.objects.get(pk=self.record_pk)
        except Record.DoesNotExist:
            self.record_pk = -1
        return super(ListRelatedImages, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.record_pk < 0:
            return self.model.objects.empty()
        else:
            return self.model.objects.filter(record=self.record_pk)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset)
        return JsonResponse(data, status=200, safe=False)
