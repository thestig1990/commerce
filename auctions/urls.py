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
    path("remove_from_watchlist/<str:title>", views.remove_from_watchlist, name="remove_from_watchlist")
]
