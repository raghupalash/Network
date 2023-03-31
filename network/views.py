import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, User_Following


def index(request):
    if request.method == "POST":
        # Extract post
        post = request.POST["post"]
        print(post)

        # Extract current user
        user = User.objects.get(pk=request.user.id)

        # Store this post
        Post.objects.create(post=post, user=user)

        return HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse('pages', args=("home", 1)))

    

def pages(request, pageName, pageNum):
    if pageName == "home":
        posts = Post.objects.all().order_by("-timestamp_created")

        template = "network/index.html"

        data = {
            "page": "home"
        }

    elif pageName == "following":
        # Extract all the relations in which current user is "following"
        relations = User_Following.objects.filter(user_A=request.user)
        
        posts = []
        for relation in relations:
            posts += Post.objects.filter(user=relation.user_B)

        # A function that returns timestamp of post
        def time_stamp(e):
            return e.timestamp_created

        posts.sort(key=time_stamp, reverse=True)

        template = "network/index.html"

        data = {
            "page": "following"
        }
    
    else:
        # Here pagename is actually username of clicked user
        clickedUser = User.objects.get(username=pageName) 

        posts = clickedUser.posts.all().order_by("-timestamp_created")

        template = "network/profilePage.html"
    
        is_following = len(User_Following.objects.filter(user_A=request.user, user_B=clickedUser))

        data = {
            "page": pageName,
            "is_following": is_following,
            "clickedUser": clickedUser,
            "followers": len(User_Following.objects.filter(user_B=clickedUser)),
            "following": len(User_Following.objects.filter(user_A=clickedUser)),
        }

    # Making a page object
    p = Paginator(posts, 10)

    # Make a list of page nums for django to iterate
    pageCount = p.num_pages
    pages = []
    for i in range(1, pageCount + 1):
        pages.append(i)
    
    return render(request, template, {
        "posts": p.page(pageNum).object_list,
        "data": data,
        "pages": pages,
        "current": pageNum
    })

def following_page(request):
    return HttpResponseRedirect(reverse("pages", args=("following", 1)))

def profile_page(request, username):
    clickedUser = User.objects.get(username=username) 

    # Follow or unfollow
    if request.method == "POST":
        if request.POST["action"] == "follow":
            User_Following.objects.create(user_A=request.user, user_B=clickedUser)
        else:
            User_Following.objects.filter(user_A=request.user, user_B=clickedUser).delete()

        return HttpResponseRedirect(reverse("profile", args=(username,)))

    return HttpResponseRedirect(reverse("pages", args=(username, 1)))
    
def edit(request, postId):
    if request.method == "PUT":
        data = json.loads(request.body)
        content = data.get("content")
        
        # Extracting the post
        post = Post.objects.get(pk=postId)

        # Making changes
        post.post = content
        post.save()

        HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "Only PUT request accepted"
        }, status=400)

def like(request, postID):
    if request.method == "GET":
        post = Post.objects.get(pk=postID)

        # Check if the user has liked the post
        if request.user in post.liked_by.all():
            likedByUser = True
        else:
            likedByUser = False


        return JsonResponse({'likes': post.likes, 'likedByUser': likedByUser}, safe=False)
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        action = data.get("action")

        # Getting the post object
        post = Post.objects.get(pk=postID)

        if action == "liked":
            # Incrementing the likes on the post
            post.likes=post.likes+1

            # This post is liked by the current user (update db)    
            post.liked_by.add(request.user)
        else:
            # Decreasing the likes on the post
            post.likes=post.likes-1

            # This post is unliked by the current user (update db)
            post.liked_by.remove(request.user)
        post.save()

        return HttpResponse(status=204)

    else:
        JsonResponse({
            "error": "Only GET and PUT reqest are accepted"
        }, status=400)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
