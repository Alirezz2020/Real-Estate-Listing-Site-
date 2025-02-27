from django.views.generic import TemplateView
from listings.models import Listing

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_listings'] = Listing.objects.order_by('-created_at')[:3]  # Show 3 latest
        return context