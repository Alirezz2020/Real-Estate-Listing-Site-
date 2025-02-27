from django import forms
from django.forms import widgets

from listings.models import Listing


class ListingForm(forms.ModelForm):
    gallery_images = forms.FileField(

        required=False,
        label='Additional Images (Gallery)'
    )

    class Meta:
        model = Listing
        fields = ['title', 'address', 'city', 'price', 'bedrooms', 'bathrooms', 'main_image']