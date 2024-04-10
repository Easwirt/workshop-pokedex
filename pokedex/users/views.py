from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm
from users.models import User  # Import your custom User model


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create a new user with the provided data
            User.objects.create_user(username=username, email=email, password=password)
            # Redirect to a success page or wherever appropriate
            return HttpResponse('User created successfully!')
    else:
        form = SignUpForm()
    return render(request, 'signup.tpl.html', {'form': form})
