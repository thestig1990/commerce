from django.contrib import admin
from .models import Listing, Bid, Comment

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
