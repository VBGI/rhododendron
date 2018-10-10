from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from .conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse, Http404
from .filters import RecordFilter
from django.urls import reverse
from .models import Record, Species, Image, Page, PhotoAlbum
from django.views.generic import DetailView, ListView
import urllib.request


def record_list(request):
    filtered_objects = RecordFilter(request.GET, queryset=Record.objects.all())
    all_filter_names = {x for x in filtered_objects.get_filters()}
    page = request.GET.get('page', 1)
    paginator = Paginator(filtered_objects.qs,
                          getattr(settings, 'RHD_PAGINATION_SIZE', 50))
    try:
        objects = paginator.get_page(page)
    except EmptyPage:
        objects = paginator.get_page(1)
    if request.is_ajax():
        data = serializers.serialize("json", objects)
        return JsonResponse(data, status=200, safe=False)
    else:
        return render(request, 'record-list.html',
                      {'objects': objects,
                      'querystring': '?' + '&'.join(('{}={}'.format(x, y) for x, y in request.GET.items() if x in all_filter_names))
                       }
                      )


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
        page = Page.objects.filter(slug=reverse('herb-data').strip('/')).first()
        return render(request,
                      'herbarium.html',
                      {'page': page}
                      )


class AlbumView(DetailView):
    model = PhotoAlbum
    http_method_names = ['get', ]
    template_name = 'show-album.html'
    content_type = 'text/html; charset=utf-8'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        dct = super().get_context_data(**kwargs)
        if self.object:
            dct.update({'images': self.object.get_images()})
        return dct

    def get_object(self, *args, **kwargs):
        try:
            obj = super().get_object(*args, **kwargs)
            self.object = obj
        except Http404:
            self.object = None
        return self.object


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
