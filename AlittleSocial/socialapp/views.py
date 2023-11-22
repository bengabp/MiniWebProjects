from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views import View
from .helpers import POSTS
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user
from django.contrib.auth import logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from uuid import uuid4



@login_required(login_url="/login")
def index(request):
    if request.method == "GET":
        return render(request, "index.html", context={
            "posts": Post.objects.all()
        })

    # Logic to create new post
    post_title = request.POST.get("post-title")
    post_body = request.POST.get("post-body")

    print(f"TITLE:{post_title}|BODY:{post_body}")
    new_post = Post(unique_id=uuid4().hex,title=post_title,body=post_body,author=request.user)
    new_post.save()
    return redirect("/")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username,password=password)
    if user is None:
        return HttpResponse("User does not exist !")
    
    print(user)

    return HttpResponse("Logged in !")


def logout(request):
    # handle user logout
    
    return redirect("/login")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    username = request.POST.get("username")
    password = request.POST.get("password")

    # Check if user exists
    user = User.objects.filter(username=username).first()
    print(user)
    if user is not None:
        return HttpResponse("User exists, login !")

    # Handle user registration
    new_user = User(username=username,password=password)
    new_user.save()

    # Login user
    login_user(request,new_user)

    return redirect("/")


@login_required(login_url="/login")
def single_post(request,unique_id):
    print("METHOD: ",request.method)
    post = Post.objects.filter(unique_id=unique_id).first()
    
    if request.method == "GET":
        if post is None:
            return HttpResponse("Post was not found !")
        print(f"Post ID => {unique_id}")
        comments = post.comment_set.all()
        return render(request,"post_details.html",context={"post":post,"comments":comments})
    comment = request.POST.get("comment")
    print(f"Comment : {comment}")
    # create a new comment object and add to the comments list for the post 
    new_comment = Comment(body=comment,author=request.user,post=post)
    new_comment.save()

    return redirect(request.path)