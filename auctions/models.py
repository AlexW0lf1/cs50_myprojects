from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Lot(models.Model):
    CATEGORIES = [(None, "No category"),
        ('EL', 'Electronics'),
        ('FS', 'Fashion'),
        ('HM', 'Home'),
        ('TY', 'Toys'),
        ('AR', 'Art'),]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.PositiveIntegerField()
    image = models.ImageField(blank=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, blank=True)
    status = models.CharField(max_length=100, default="Active")
    watching = models.ManyToManyField(User, blank=True, related_name="watchlist")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lots")

class Bid(models.Model):
    price = models.PositiveIntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")