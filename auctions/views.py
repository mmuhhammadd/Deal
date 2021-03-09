from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Q
from .models import User, Categories, Listings, Watchlist, Bids, Comments
from django.contrib.auth.decorators import login_required

class CreateListing(forms.Form):
    title = forms.CharField(label='Title', max_length=64)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    price = forms.DecimalField(label="Starting Bid", max_digits=7, decimal_places=2)
    url = forms.URLField(label="URL for image", widget=forms.URLInput, required=False)
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label='Category', initial='Select')


def index(request):
    listings = Listings.objects.filter(status="Active")
    return render(request, "auctions/index.html", {"listings": listings})


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
def create_listing(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {"notlogged": "You must login first!"})
    categories = Categories.objects.all()
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():

            username = request.user.username
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]

            listing = Listings(user=User.objects.get(username=username), title=title, description=description,initial_price=price,current_price=price,url=url,category=category)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {"categories": categories, "form": CreateListing()})

    return render(request, "auctions/create.html", {"categories": categories, "form": CreateListing()})

def mylistings(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {"notlogged": "You must login first!"})
    user = User.objects.get(username=request.user.username)
    listings = Listings.objects.filter(user=user)
    return render(request, "auctions/mylistings.html", {"listings":listings})

def listing(request, id):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        listing = Listings.objects.get(id=id) 
        exist = Watchlist.objects.filter(user=user, listing=listing)
        bids = Bids.objects.filter(item=listing, bid=listing.current_price)
        userbid = Bids.objects.filter(item=listing, user=user)
        comments = Comments.objects.filter(item=listing)
        if request.method == "POST":
            if "add" in request.POST:
                watchlist = Watchlist(user=user, listing=listing)
                watchlist.save()
                return render(request, "auctions/listing.html", {"listing": listing, "exist": exist, "user": user, "bids": bids, "userbid": userbid, "comments":comments})
            if "remove" in request.POST:
                exist.delete()
                return render(request, "auctions/listing.html", {"listing": listing, "exist": exist, "user": user, "bids": bids, "userbid": userbid, "comments":comments})
            if "close" in request.POST:
                listing.status = "Closed"
                listing.save()
                return render(request, "auctions/listing.html", {"listing": listing, "exist": exist, "user": user, "bids": bids, "userbid": userbid, "comments":comments})
            if "bid" in request.POST:
                bid = request.POST.get("bid")
                if int(bid) <= listing.current_price:
                    return render(request, "auctions/listing.html", {"listing": listing, "exist": exist, "user": user, "bids": bids, "userbid": userbid, "comments":comments, "message": "Bid must be greater than current best offer."})
                else:
                    searchbid = Bids.objects.filter(user=user,item=listing)
                    if not searchbid:
                        newbid = Bids(user=user, item=listing, bid=bid)
                        newbid.save()
                        listing.current_price = bid
                        listing.save()
                    else:
                        for singlebid in searchbid:
                            singlebid.bid = bid
                            singlebid.save()
                            if listing.current_price < int(singlebid.bid):
                                listing.current_price = singlebid.bid
                                listing.save()
                    return render(request, "auctions/listing.html", {"listing": listing, "exist": exist, "user": user, "bids": bids, "userbid": userbid, "comments":comments})
            if "comment" in request.POST:
                comment = request.POST.get("comment")
                addcomment = Comments(user=user, item=listing, Comment=comment)
                addcomment.save()
                return render(request, "auctions/listing.html", {"listing": listing, "exist": exist, "user": user, "bids": bids, "userbid": userbid, "comments":comments})

        return render(request, "auctions/listing.html", {"listing": listing, "exist": exist, "user": user, "bids": bids, "userbid": userbid, "comments":comments})
    else:
        listing = Listings.objects.get(id=id) 
        return render(request, "auctions/listing1.html", {"listing": listing})

def mybids(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {"notlogged": "You must login first!"})
    username = request.user.username
    user = User.objects.get(username=username)
    bids = Bids.objects.filter(user=user)
    return render(request, "auctions/mybids.html", {"bids": bids})

def watchlist(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {"notlogged": "You must login first!"})
    username = request.user.username
    user = User.objects.get(username=username)
    watchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist, "user": user})

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})

def category(request, id):
    category = Categories.objects.get(id=id)
    listings = Listings.objects.filter(category=category)

    return render(request, "auctions/category.html", {"listings": listings})
