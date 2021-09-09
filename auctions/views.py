from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.expressions import F
from django.db.models.fields import DecimalField, FloatField, IntegerField
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import response
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import *
from .models import *
from django.db.models import Count, F
from django.urls.base import reverse_lazy


def index(request):
    #get the users
    username = User.objects.all()
    #get the listing and see if user is login or not differ view
    if request.user.is_authenticated:
        listing = Listing.objects.all()
    else:
        listing = Listing.objects.filter(closed=False)
    
    return render(request, "auctions/index.html", {
        "listing": listing,
        "username": username,
        'title': "Active Listings",
    })

@login_required
def create(request):
    template_name = 'auctions/create.html'
    success_url = reverse_lazy('auctions:index')

    if request.method == 'GET':
        form = MainForm()
        ctx = {'form': form}
        return render(request, template_name, ctx)

    if request.method == 'POST':
        form = MainForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, template_name, ctx)

        # Add owner to the model before saving
        list = form.save(commit=False)
        list.user = request.user
        list.save()
        return redirect(success_url)



@login_required
def listing(request, list_id):
    success_url = reverse_lazy('auctions:index')
    #Get the listitem from models
    list = Listing.objects.get(pk=list_id)
    #Get the bid value from the models from current list
    bid = Bid(user=request.user, list=list)
    #Get the bidform and create instance
    bidform = BidForm(request.POST, instance=bid)    

    #Getting input of bid form and save it with user.
    if request.method == 'POST':
        # check if the form is valid
        if bidform.is_valid():
            bidobj = bidform.save(commit=False)
            # logged in user is available on a view func's `request` instance
            bidobj.user = request.user
            bidobj.save()  # safe to save w/ user in tow
            
        else:
            return render(request, "auctions/listing.html", {
                "message": "Invalid bid.",
                'list': list,
                'form': bidform
            })

        return HttpResponseRedirect(success_url)
    else:
        #Get the bidform from froms.models file.
        form = BidForm()
        return render(request, "auctions/listing.html", {
            'list': list,
            'form': form,
            'is_watch': request.user.watchlist.filter(pk=list_id).exists()
        })

@login_required
def comment(request, list_id):
    #get the list item    
    list = Listing.objects.get(pk=list_id)    
    #Get the comment value from the models from current list
    comment = Comment(user=request.user, list=list)
    #Get the commentform and create instance
    comform = CommentForm(request.POST, instance=comment)    

    if request.method == "POST":
        if comform.is_valid():
            comobj = comform.save(commit=False)
            # logged in user is available on a view func's `request` instance
            comobj.user = request.user
            comobj.save()  # safe to save w/ user in tow
    else:
        #Get the comment forms.model for input.
        comform = CommentForm()
        return render(request, "auctions/comment.html", {
            'list': list,
            'comform': comform
        })
    return HttpResponseRedirect(reverse("comment", args=(list_id,)))

@login_required
def watchlist(request, list_id):
    #cheching the user if authentic
    assert request.user.is_authenticated
    user = request.user
    #Geting the list objects via ID
    listing = Listing.objects.get(pk=list_id)
    
    #Toggel if watchlist or nowt
    if user.watchlist.filter(pk=list_id).exists():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    
    return render(request, "auctions/index.html", {
        'listing': request.user.watchlist.all(),
        'title': "Watchlist Items",
        'is_watch': request.user.watchlist.filter(pk=list_id).exists()
    })

@login_required
def watchlistitems(request):
    return render(request, "auctions/index.html", {
        'listing': request.user.watchlist.all(),
        'title': "Watchlist Items",
        'is_watch': request.user.watchlist.filter().exists()
    })

@login_required
def closed(request, list_id):
    #Get the list item by id.
    list = Listing.objects.get(pk=list_id)
    #check the if the user and request users are same or not
    if request.user == list.user:
        list.closed = True
        list.save()
    else:
        return render(request, "auctions/listing.html", {
                'list':list,
                "message": "Sorry! you can not close this item."
            })        
    
    return render(request, "auctions/listing.html", {
        'list': list,
        "message": "Item is closed.",
        'title': "This Listing is closed"
    })

def category(request, category):
    #get the catg filter via str 
    listings = Listing.objects.filter(closed=False, category=category)
    #Show the catg Buttons on screen via str repres
    categories = list(set([listing.category for listing in Listing.objects.all() if listing.category]))
    return render(request, "auctions/categories.html", {
        'category': category,
        'listing': listings,
        'categories': categories,
        'title': "Product Categories",
    })

def categories(request):
    #Show the catg on screen via str represent
    categories = list(set([listing.category for listing in Listing.objects.all() if listing.category]))
    return render(request, "auctions/categories.html", {
        'categories': categories,
        'title': "Product Categories",
    })

def stream_file(request, pk):
    list = get_object_or_404(Listing, id=pk)
    response = HttpResponse()
    response['Content-Type'] = list.content_type
    response['Content-Length'] = len(list.picture)
    response.write(list.picture)
    return response