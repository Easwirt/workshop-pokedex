from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
from users.models import User  # Import your custom User model
from django.contrib.auth import login, authenticate, logout


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return HttpResponse('User created successfully!')
    else:
        form = SignUpForm()
    return render(request, 'signup.tpl.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.tpl.html', {'form': form, 'error': 'Invalid login'})
    else:
        form = LoginForm()
    return render(request, 'login.tpl.html', {'form': form})

def signout(request):
    logout(request)
    return redirect("/")
