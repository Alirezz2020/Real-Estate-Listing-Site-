from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Listing, Gallery
from .forms import ListingForm
from decimal import Decimal, DecimalException
from django.db.models import Q
from django.views.generic import ListView
from .models import Listing

class IndexView(ListView):
    model = Listing
    template_name = 'listings/index.html'
    context_object_name = 'listings'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        min_price = self.request.GET.get('min_price', '0')
        max_price = self.request.GET.get('max_price', '9999999')
        bedrooms = self.request.GET.get('bedrooms', '0')
        bathrooms = self.request.GET.get('bathrooms', '0')

        # Convert min_price and max_price to Decimal
        try:
            min_price = Decimal(min_price)
        except (DecimalException, ValueError):
            min_price = Decimal('0')

        try:
            max_price = Decimal(max_price)
        except (DecimalException, ValueError):
            max_price = Decimal('9999999')

        # Convert bedrooms and bathrooms to integers
        try:
            bedrooms = int(bedrooms)
        except (ValueError, TypeError):
            bedrooms = 0

        try:
            bathrooms = int(bathrooms)
        except (ValueError, TypeError):
            bathrooms = 0

        # Build and filter queryset
        queryset = Listing.objects.all()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(city__icontains=query) |
                Q(address__icontains=query)
            )

        queryset = queryset.filter(
            price__gte=min_price,
            price__lte=max_price,
            bedrooms__gte=bedrooms,
            bathrooms__gte=bathrooms
        ).order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Update context with filter parameters to maintain state
        context.update({
            'min_price': self.request.GET.get('min_price', '0'),
            'max_price': self.request.GET.get('max_price', '9999999'),
            'bedrooms': self.request.GET.get('bedrooms', '0'),
            'bathrooms': self.request.GET.get('bathrooms', '0'),
            'query': self.request.GET.get('q', '')
        })
        return context




class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/detail.html'


class SearchView(ListView):
    model = Listing
    template_name = 'listings/search.html'
    context_object_name = 'listings'
    paginate_by = 12  # Add pagination for search results

    def get_queryset(self):
        query = self.request.GET.get('q')
        min_price = self.request.GET.get('min_price', 0)
        max_price = self.request.GET.get('max_price', 9999999)
        bedrooms = self.request.GET.get('bedrooms', 0)
        bathrooms = self.request.GET.get('bathrooms', 0)

        queryset = Listing.objects.filter(
            Q(title__icontains=query) |
            Q(city__icontains=query) |
            Q(address__icontains=query)
        )

        # Apply numeric filters
        queryset = queryset.filter(
            price__gte=min_price,
            price__lte=max_price,
            bedrooms__gte=bedrooms,
            bathrooms__gte=bathrooms
        ).order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'min_price': self.request.GET.get('min_price', 0),
            'max_price': self.request.GET.get('max_price', 9999999),
            'bedrooms': self.request.GET.get('bedrooms', 0),
            'bathrooms': self.request.GET.get('bathrooms', 0),
        })
        return context
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
        return get_object_or_404(User, username=self.kwargs['username'])