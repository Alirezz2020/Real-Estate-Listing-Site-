from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    main_image = models.ImageField(upload_to='listings/')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    listing = models.ForeignKey(Listing, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listings/gallery/')

    def __str__(self):
        return f"Image for {self.listing.title}"