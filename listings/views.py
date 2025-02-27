from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Listing
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Listing, Gallery
from .forms import ListingForm

class IndexView(ListView):
    model = Listing
    template_name = 'listings/index.html'
    context_object_name = 'listings'
    paginate_by = 12
    ordering = ['-created_at']


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/detail.html'


class SearchView(ListView):
    model = Listing
    template_name = 'listings/search.html'
    context_object_name = 'listings'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Listing.objects.filter(
                Q(title__icontains=query) |
                Q(city__icontains=query) |
                Q(address__icontains=query)
            ).order_by('-created_at')
        return Listing.objects.none()
class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('listings:index')

    def form_valid(self, form):
        form.instance.agent = self.request.user
        response = super().form_valid(form)

        # Handle gallery images
        images = self.request.FILES.getlist('gallery_images')
        for image in images:
            Gallery.objects.create(listing=self.object, image=image)
        return response


class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('listings:index')

    def test_func(self):
        return self.request.user == self.get_object().agent or self.request.user.is_superuser

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add new gallery images
        images = self.request.FILES.getlist('gallery_images')
        for image in images:
            Gallery.objects.create(listing=self.object, image=image)
        return response


class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    success_url = reverse_lazy('listings:index')
    template_name = 'listings/listing_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().agent or self.request.user.is_superuser



class ContactAgentView(DetailView):
    model = User  # Assumes agents are stored as Django Users
    template_name = 'listings/agent_contact.html'
    context_object_name = 'agent'

    def get_object(self, queryset=None):
        listing = get_object_or_404(Listing, pk=self.kwargs['pk'])
        return listing.agent