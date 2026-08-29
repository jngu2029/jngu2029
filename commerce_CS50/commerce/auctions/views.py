from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
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

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        # create new listing
        listing = Listing.objects.create(
            title = request.POST["title"],
            picture = request.POST["picture"],
            description = request.POST["description"],
            price = request.POST["price"],
            owner = request.user
        )
        # redirect to index page showing the active listings
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html")

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "status": 404,
            "message": "Listing not found",
            "watchlist_count" : request.user.watchlist.all().count()
        }, status=404)
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_min": float(listing.price) + 0.01,
        "is_watching": (
            request.user.is_authenticated
            and listing.watchers.filter(pk=request.user.pk).exists()
        )
    })

@login_required(login_url="login")
def watchlist(request):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=request.POST["listing_id"])
        except Listing.DoesNotExist:
            return render(request, "auctions/error.html", {
                "status": 404,
                "message": "Listing not found",
            }, status=404)
            
        if request.POST["action"] == "add":
            listing.watchers.add(request.user)
        elif request.POST["action"] == "remove":
            listing.watchers.remove(request.user)
            
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))

    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all(),
    })
