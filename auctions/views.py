from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ValidationError

from .models import User, Lot, Bid, Comment


class NewLotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ['title', 'description', 'price', 'image', 'category']


class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price',]


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment',]


def index(request):
    lots = Lot.objects.filter(status="Active")
    return render(request, "auctions/index.html", {
        "lots": lots,
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


@login_required(login_url='/login')
def new(request):
    if request.method == "POST":
        # Create form instance from POST data
        form = NewLotForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('image')
            print(img)
            # Save a new lot (model instance)
            new_lot = form.save(commit=False)
            new_lot.seller = request.user
            new_lot.status = "Active"
            print(new_lot.image)
            new_lot.save()
            print(new_lot)
            return HttpResponseRedirect(reverse("listing", args=(new_lot.id,)))
        else:
            return render(request, "auctions/new.html", {
                "form": form,
                "message": "Invalid form data",
            })

    return render(request, "auctions/new.html", {
        "form": NewLotForm(),
    })

def listing(request, lot_id):
    lot = Lot.objects.get(pk=lot_id)
    message = ""
    if request.method == "POST":
        if request.POST.get("price"):
            form = NewBidForm(request.POST)
            if form.is_valid():
                new_bid = form.save(commit=False)
                new_bid.buyer = request.user
                new_bid.lot = lot
                try:
                    new_bid.save()
                except ValidationError:
                    return render(request, "auctions/error.html", {
                        "message": "Bid has to be higher than current price",
                    })

            else:
                bids = lot.bids.all()
                comments = lot.comments.all()
                return render(request, "auctions/lot.html", {
                    "lot": lot,
                    "bids": bids,
                    "comments": comments,
                    "form_bid": NewBidForm(request.POST),
                    "form_comment": NewCommentForm(),
                })

        if request.POST.get("comment"):
            form = NewCommentForm(request.POST)
            if form.is_valid():
               new_comment = form.save(commit=False)
               new_comment.author = request.user
               new_comment.lot = Lot.objects.get(pk=lot_id)
               new_comment.save()
            else:
                bids = lot.bids.all()
                comments = lot.comments.all()
                return render(request, "auctions/lot.html", {
                    "lot": lot,
                    "bids": bids,
                    "comments": comments,
                    "form_bid": NewBidForm(),
                    "form_comment": NewCommentForm(request.POST),
                })
        if request.POST.get("close") and request.user == Lot.objects.get(pk=lot_id).seller:
            lot.status = "Closed"
            if lot.bids:
                lot.winner = lot.bids.last().buyer
    if lot:
        if lot.status == 'Closed' and request.user == lot.seller:
            message = "You sold that listing for $" + lot.price
        bids = lot.bids.all()
        comments = lot.comments.all()
        return render(request, "auctions/lot.html", {
            "lot": lot,
            "bids": bids,
            "comments": comments,
            "form_bid": NewBidForm(),
            "form_comment": NewCommentForm(),
            "message": message,
        })
    else:
        return render(request, "auctions/error.html", {
            "message": "Unexisting lot",
        })


@login_required(login_url='/login')
def watchlist_view(request):
    user = request.user
    if request.method == "POST":
        form = request.POST
        if form.get("add"):
            user.watchlist.add(Lot.objects.get(pk=form.get("lot_id")))
        if form.get("remove"):
            user.watchlist.remove(Lot.objects.get(pk=form.get("lot_id")))
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
    })


def category_view(request, category):
    lots = Lot.objects.filter(category=category, status="Active")
    return render(request, "auctions/category.html", {
        "lots": lots,
        "category": category,
    })


def your_listings(request):
    user = request.user
    lots = user.lots.all()
    print(lots)
    return render(request, "auctions/your_lots.html", {
        "lots": lots,
    })