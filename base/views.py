from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateUserForm
from .models import Language


def home_page(request):
    return render(request, 'base/index.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('posts-page')
            else:
                messages.error(request, 'Password is wrong!')
        except:
            messages.error(request, 'Username is wrong!')
    return render(request, 'base/login.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')


def register_page(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid:
            try:
                form.save()
                return redirect('posts-page')
            except:
                messages.error(request, 'Something went wrong')
    form = CreateUserForm()
    return render(request, 'base/register.html', {"form": form})


def profile_page(request):
    user = request.user
    posts = Language.objects.filter(user__id=user.id)
    # posts = Language.objects.filter(user = user)
    post_length = len(posts)
    return render(request, 'base/profile.html', {"user": user, "posts": posts, "post_length": post_length})


def other_profile_page(request, id):
    user = User.objects.get(id=id)
    posts = Language.objects.filter(user__id=user.id)
    post_length = len(posts)
    return render(request, 'base/profile.html', {"user": user, "posts": posts, "post_length": post_length})
