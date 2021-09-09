import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core import serializers
from django.views import View
from .models import *
from .forms import *

@csrf_exempt
def index(request):
    success_url = reverse_lazy('network:index')
    if request.method == "POST":
        form = PostForm(request.POST)
        # Attempt to create new user
        if form.is_valid():
            newobj = form.save(commit=False)
            # logged in user is available on a view func's `request` instance
            newobj.user = request.user
            newobj.save()  # safe to save w/ user in tow
            return HttpResponseRedirect(success_url)
    #Show the post form to user
    form = PostForm()
    #All posts via revers order
    pub_posts = Posts.objects.all().order_by('-pub_date')
    
    #paginator 
    paginator = Paginator(pub_posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj":page_obj,
        "form": form,
    })

#Show the user profile
def profile(request, user_id):
    user = request.user
    curuser = get_object_or_404(Profile, user=user)
    profile = get_object_or_404(Profile, user=user_id)
    posts = Posts.objects.filter(user=user_id)

    #paginator 
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile": profile,
        "page_obj": page_obj,
        "curuser": curuser
    })  

#Show the users who currently follows you
@login_required
@csrf_exempt
def following(request):
    user = request.user
    #get the porfile user via user id
    user = Profile.objects.get(user=user.id)
    
    #Check if the user follow you 
    following = user.follow.all().values_list('user', flat=True)
    posts = Posts.objects.filter(user__in=following).order_by('-pub_date')

    #follower details.
    follow = user.follow.all()

    #paginator 
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/following.html", {
        "follow": follow,
        "page_obj": page_obj,
    })  


# To complete the user its profile if user want
@login_required
@csrf_exempt
def edit_profile(request, user_id):
    success_url = reverse_lazy('network:profile', kwargs={'user_id':user_id})

    if request.method == "GET":
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileForm(instance=profile)
        ctx = {'form': form}
        return render(request, "network/edit_profile.html", ctx)

    if request.method == "POST":
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileForm(request.POST, request.FILES or None, instance=profile)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, "network/edit_profile.html", ctx)

        profile = form.save(commit=False)
        profile.save()

        return redirect(success_url)


#follow and unfollow button
def follow(request, user_id):
    success_url = reverse_lazy('network:profile', kwargs={'user_id': user_id})

    #User current
    user = request.user
    oneprofile = user.id

    #User to be followed
    profile = Profile.objects.get(user=user_id)
    
    #Toggle the add and remove button
    if profile.follow.filter(user=oneprofile).exists():
        profile.follow.remove(oneprofile)
    else:
        profile.follow.add(oneprofile)
    
    return HttpResponseRedirect(success_url)


def posts(request):
    pub_posts = Posts.objects.all().order_by('-pub_date')
    #paginator 
    paginator = Paginator(pub_posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj":page_obj,
    })
@login_required
@csrf_exempt
def edit(request, post_id):
    post = Posts.objects.get(id=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.post = data["post"]
        post.save()
        return HttpResponse(status=204)

@login_required
@csrf_exempt
def comment(request, post_id):
    post = Posts.objects.get(id=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.reply = data["post"]
        post.save()
        return HttpResponse(status=204)


@login_required
@csrf_exempt
def like(request, post_id):
    #User to be followed
    post = Posts.objects.get(pk=post_id)
    #Send the jsondata
    if request.method == "GET":
        return JsonResponse(post.serialize())
    #User current
    user = request.user
    oneprofile = user.id
    #liked = True
    if request.method == "PUT":
        liked = request.POST.get('liked')
        #Toggle the add and remove button
        if post.like.filter(pk=oneprofile).exists():
            post.like.remove(oneprofile)
            liked = "Like"
        else:
            post.like.add(oneprofile)
            liked = "Liked"
        
        return JsonResponse({'liked': liked,'total_like': post.like.count(), "status": 201})
"""
@csrf_exempt
def login_view(request):
    success_url = reverse_lazy('network:index')

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(success_url)
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    success_url = reverse_lazy('network:index')
    return HttpResponseRedirect(success_url)
"""

def register(request):
    success_url = reverse_lazy('network:index')
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match.",
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken.",
            })
        login(request, user)
        
        # create profile User
        user = request.user
        profile = Profile(user=user)
        profile.save()

        return HttpResponseRedirect(success_url)
    else:
        return render(request, "network/register.html", {
        })

def stream_file(request, pk):
    prof = get_object_or_404(Profile, id=pk)
    response = HttpResponse()
    response['Content-Type'] = prof.content_type
    response['Content-Length'] = len(prof.picture)
    response.write(prof.picture)
    return response