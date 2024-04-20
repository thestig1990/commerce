from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# @login_required
def create_listing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            starting_bid = request.POST["bid"]
            image_url = request.POST["url"]
            category = request.POST["category"]

            try:
                listing = Listing.objects.create(
                    title=title,
                    description=description,
                    starting_bid=int(starting_bid),
                    image=image_url,
                    category=category
                )
            except:
                return render(request, "auctions/create_listing.html", {
                    "message": "Some message."
                })
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html")

    else:
        return render(request, "auctions/create_listing.html", {
            "message": "Please login first using the link in the navigation bar"
        })


def listing_detail(request, title):
    listing = get_object_or_404(Listing, title=title)
    
    context = {
    "listing": listing,
    }

    return render(request, "auctions/listing_detail.html", context)


@login_required
def add_to_watchlist(request, title):
    user = request.user
    listing = get_object_or_404(Listing, title=title)
    
    if listing in user.watchlist.all():
        return redirect('listing-detail', title=title)
    
    user.watchlist.add(listing)
    messages.success(request, "The item has been successfully added to the Watchlist.")
    
    return redirect('listing-detail', title=title)


@login_required
def remove_from_watchlist(request, title):
    user = request.user
    listing = get_object_or_404(Listing, title=title)
    
    if listing not in user.watchlist.all():
        return redirect('listing-detail', title=title)
    
    user.watchlist.remove(listing)
    messages.success(request, "The item has been successfully deleted from the Watchlist.")
    
    return redirect('listing-detail', title=title)