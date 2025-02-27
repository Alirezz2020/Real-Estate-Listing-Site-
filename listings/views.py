from django.views.generic import ListView, DetailView
from .models import Listing
from django.db.models import Q
from django.core.paginator import Paginator


class IndexView(ListView):
    model = Listing
    template_name = 'listings/index.html'
    context_object_name = 'listings'
    paginate_by = 12


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/detail.html'


class SearchView(ListView):
    model = Listing
    template_name = 'listings/search.html'
    context_object_name = 'listings'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Listing.objects.filter(
            Q(title__icontains=query) | Q(city__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context