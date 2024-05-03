from django.contrib import admin
from .models import Listing, Bid, Comment

# Register your models here.
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "listing", "user", "timestamp")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "listing", "user", "timestamp")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "starting_bid", "user", "closed_at", "winner")


admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
