from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid, Comment


def index(request):
    # Get all listing objects
    listings = Listing.objects.all()

    # Create a dict where the last highest bids for each listing are saved
    last_bids = {}

    # For each listing get the last highest bid if it exist
    for listing in listings:
        try:
            highest_bid = listing.bids.order_by("-amount").first().amount
        except AttributeError:
            highest_bid = None
        last_bids[listing.title] = highest_bid
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "last_bids": last_bids,
    })


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
            user = request.user

            try:
                Listing.objects.create(
                    title=title,
                    description=description,
                    starting_bid=int(starting_bid),
                    image=image_url,
                    category=category,
                    user=user
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
    # Get a listing object by its title
    listing = get_object_or_404(Listing, title=title)

    # Get the last highest bid for the listing if it exist
    try:
        highest_bid = listing.bids.order_by("-amount").first().amount
    except AttributeError:
        highest_bid = None

    if highest_bid is None:
        start_bid = listing.starting_bid
    else:
        start_bid = None

    # Get all listing comments
    comments = listing.comments.all()

    # Get the number of bids for the current listing
    bids_count = listing.bids.count()

    # Get the highest bid object
    bid_obj = listing.bids.order_by("-amount").first()
    
    context = {
    "listing": listing,
    "highest_bid": highest_bid,
    "start_bid": start_bid,
    "comments": comments,
    "bids_count": bids_count,
    "bid_obj": bid_obj,
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


@login_required
def place_bid(request, title):
    # Get a listing object by its title
    listing = get_object_or_404(Listing, title=title)

    # Get the starting bid for the listing
    start_bid = listing.starting_bid
    
    # Get a highest bid for the listing
    try:
        highest_bid = listing.bids.order_by('-amount').first().amount
    except AttributeError:
        highest_bid = start_bid      

    if request.method == "POST":
        bid_amount = request.POST["bid_amount"]

        try:
            bid_amount = int(bid_amount)
        except ValueError:
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "error_message": "Invalid bid amount. Please enter an integer number.",
                "highest_bid": highest_bid,
                "start_bid": start_bid,
            })

        if bid_amount <= listing.starting_bid:
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "error_message": "Bid amount must be greater than the starting bid - " + str(listing.starting_bid) + "$.",
                "highest_bid": highest_bid,
                "start_bid": start_bid,
            })

        if listing.bids.exists() and bid_amount <= listing.bids.order_by('-amount').first().amount:
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "error_message": "Bid amount must be greater than the current highest bid - " + str(listing.bids.order_by('-amount').first().amount) + "$.",
                "highest_bid": highest_bid,
                "start_bid":  start_bid,
            })

        # Save bid
        bid = Bid(user=request.user, listing=listing, amount=bid_amount)
        bid.save()

        return HttpResponseRedirect(reverse("listing-detail", args=(listing.title,)))
    else:
        return redirect("listing-detail", title=title)


@login_required
def add_comment(request, title):
    # Get listing object by its title
    listing = get_object_or_404(Listing, title=title)

    if request.method == "POST":
        comment = request.POST["comment"]

        # Save comment
        comment_obj = Comment(comment=comment, listing=listing, user=request.user)
        comment_obj.save()
        return redirect("listing-detail", title=title)
    else:
        return redirect("listing-detail", title=title)


def close_auction(request, title):
    # Get listing object by its title
    listing = get_object_or_404(Listing, title=title)

    # Check if the current user is the author of the auction
    if listing.user == request.user:
        if not listing.is_closed:  # check if the auction is not closed
            highest_bid = listing.bids.order_by('-amount').first()  # get highest bid for the listing object
            if highest_bid:  # check if bids are present in the auction
                # Determine the winner
                listing.winner = highest_bid.user
                # Calling the close method from the Listing model
                listing.close()
            return redirect("listing-detail", title=title)
    return redirect("index")