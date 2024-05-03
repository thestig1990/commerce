from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    image = models.URLField(blank=True)
    category = models.CharField(
        max_length=2,
        blank=True,
        choices=CATEGORY_CHOICES,
        default=DRONES,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="listings")
    closed_at = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_auctions")

    @property
    def is_closed(self):
        return self.closed_at is not None

    def close(self):
        if not self.closed_at:
            self.closed_at = timezone.now()
            self.save()
    
    def __str__(self):
        return f"{self.id}: {self.title} --> Starting bid - {self.starting_bid}, Category - {self.category}."


class Bid(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="users")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bid - {self.amount}$; per Listing - {self.listing.title}; User - {self.user.username}."


class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment - {self.comment}; per Listing {self.listing.title}; User - {self.user.username}."