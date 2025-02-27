from django.urls import path
from .views import IndexView, ListingDetailView, SearchView

app_name = 'listings'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', ListingDetailView.as_view(), name='detail'),
    path('search/', SearchView.as_view(), name='search'),
]