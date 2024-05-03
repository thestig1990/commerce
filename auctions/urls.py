from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.create_listing, name="create-listing"),
    path("listing/<str:title>", views.listing_detail, name="listing-detail"),
    path("add_to_watchlist/<str:title>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<str:title>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("place_bid/<str:title>", views.place_bid, name="place_bid"),
    path("add_comment/<str:title>", views.add_comment, name="add_comment"),
    path("close_auction/<str:title>", views.close_auction, name="close_auction"),
    path("wachlist", views.show_watchlist, name="show_watchlist"),
    path("categories/<str:category>", views.listings_by_category, name="listings_by_category"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
]
