# listings/urls.py
from django.urls import path
from .views import IndexView, ListingDetailView, SearchView, ListingCreateView, ListingUpdateView, ListingDeleteView, \
    ContactAgentView

app_name = 'listings'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', ListingDetailView.as_view(), name='detail'),
    path('add/', ListingCreateView.as_view(), name='add'),
    path('<int:pk>/update/', ListingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ListingDeleteView.as_view(), name='delete'),
    path('search/', SearchView.as_view(), name='search'),
    path('<int:pk>/contact/', ContactAgentView.as_view(), name='contact_agent'),
    path('<int:pk>/contact/', ContactAgentView.as_view(), name='contact_agent'),
]