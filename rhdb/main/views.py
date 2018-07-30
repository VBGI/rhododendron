from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
from .filters import RecordFilter
from .models  import Record, Species, Image
from django.views.generic import DetailView, ListView


def record_list(request):
    filtered_objects = RecordFilter(request.GET, queryset=Record.objects.all())
    page = request.GET.get('page', 1)
    objects = Paginator(filtered_objects.qs,
                        getattr(settings, 'RHD_PAGINATION_SIZE', 50))
    try:
        objects = objects.page(page)
    except EmptyPage:
        objects = objects.page(1)
    return render(request, 'list.html',
                  {'objects': objects},
                  content_type='text/plain; charset utf-8')


class SpeciesDetail(DetailView):
    model = Species
    template_name = 'species-details.html'


class RecordDetail(DetailView):
    model = Record
    template_name = 'record-details.html'


# class ListRelatedImages(ListView):
#     # TODO: Should return json-reponse, -- a set of all images related with the current record.
#     model = Image
#     template_name= 'image-datails.html'
