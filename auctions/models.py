from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlist")


class Listing(models.Model):
    DRONES = 'DR'
    ELECTRONICS = 'EL'
    FASHION = 'FA'
    HOME = 'HO'
    TOYS = 'TO'
    CATEGORY_CHOICES = [
        (DRONES, 'Drones'),
        (ELECTRONICS, 'Electronics'),
        (FASHION, 'Fashion'),
        (HOME, 'Home'),
        (TOYS, 'Toys'),
    ]
    title = models.CharField(max_length=32)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image = models.ImageField(blank=True)
    category = models.CharField(
        max_length=2,
        blank=True,
        choices=CATEGORY_CHOICES,
        default=DRONES,
    )
    
    def __str__(self):
        return f"{self.id}: {self.title.split(" ")[0]} --> Starting bid - {self.starting_bid}, Category - {self.category}."


class Bid(models.Model):
    bid = models.IntegerField()
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="auction")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user")
    
    def __str__(self):
        return f"{self.id} - {self.bid}."


class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"{self.id} - {self.comment}."