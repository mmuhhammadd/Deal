from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    Active = 'Active'
    Closed = 'Closed'
    ListingStatusChoices= [
    (Active, 'Active'),
    (Closed, 'Closed')
    ]

    user = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    initial_price = models.DecimalField(max_digits=7, decimal_places=2)
    current_price = models.DecimalField(max_digits=7, decimal_places=2)
    url = models.URLField(blank=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT, related_name="listings")
    status = models.CharField(max_length=64, choices=ListingStatusChoices, default=Active)

class Bids(models.Model):
    user = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey('Listings', to_field='id', on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=7, decimal_places=2)

class Comments(models.Model):
    user = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    item = models.ForeignKey('Listings', to_field='id', on_delete=models.CASCADE, related_name="comments")
    Comment = models.TextField(blank=False)

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Watchlist(models.Model):
        user = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE, related_name="watchlist")
        listing = models.ForeignKey('Listings', on_delete=models.CASCADE)

