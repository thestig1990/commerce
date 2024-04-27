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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="listings")
    
    def __str__(self):
        return f"{self.id}: {self.title.split(" ")[0]} --> Starting bid - {self.starting_bid}, Category - {self.category}."


class Bid(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="users")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Id: {self.id}; {self.amount}$ per Listing - {self.listing.title} and User - {self.user.username}."


class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Id: {self.id}; comment - {self.comment}; per Listing {self.listing.title} from User - {self.user.username}."