from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Lot(models.Model):
    CATEGORIES = [(None, "No category"),
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Home', 'Home'),
        ('Toys', 'Toys'),
        ('Art', 'Art'),]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.PositiveIntegerField()
    image = models.ImageField(blank=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, blank=True)
    status = models.CharField(max_length=100, default="Active")
    created = models.DateField(auto_now_add=True)
    watching = models.ManyToManyField(User, blank=True, related_name="watchlist")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lots")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self) -> str:
        return f"{self.title}, {self.seller}, {self.created}"

class Bid(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="bids")
    price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.lot}, {self.buyer}, {self.price}"

    def save(self):
        lot = self.lot
        print(self.price)
        print(lot.price)
        if self.price <= lot.price:
            raise ValidationError('Bid has to be larger than current price')
        else:
            super().save()
            lot.price = self.price
            lot.save()


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self) -> str:
        return f"{self.lot}, {self.author}, {self.comment}"