from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .models import User, EmailVerificationToken, Profile
from .tokens import email_verification_token
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists! Please try a different username.")
                mistake = "Username already exists! Please try a different username."
                return render(request, "auth/signupbad.tpl.html", context={'mistake': mistake})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                mistake = "Email already registered!"
                return render(request, "auth/signupbad.tpl.html", context={'mistake': mistake})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
        
            verification_token = email_verification_token.make_token(user)
            EmailVerificationToken.objects.create(user=user, token=verification_token)
            verification_link = f'127.0.0.1:8000/auth/emailverification/{urlsafe_base64_encode(force_bytes(user.pk))}/{verification_token}'
            
            subject = "Please verify your email address..."
            message = f"Hello {user.username},\n\nPlease click on the link below to verify your email address:\n\n{verification_link}"
            email = EmailMessage(subject, message, to=[email])
            email.send()

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
                mistake = "Invalid username or password"
                return render(request, 'auth/signupbad.tpl.html', {'mistake': mistake})
    else:
        form = LoginForm()
    return render(request, 'login.tpl.html', {'form': form})

def signout(request):
    logout(request)
    return redirect("/")


def email_verification(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        token_obj = EmailVerificationToken.objects.get(user=user)
    except (User.DoesNotExist, EmailVerificationToken.DoesNotExist):
        user = None
        token_obj = None

    if user is not None and token_obj is not None and token_obj.token == token:
        user.is_active = True
        user.save()
        login(request, user)
        message = "Your email has been verified."
        return render(request, 'auth/emailverified.tpl.html', {'message' : message})
    else:
        message = "Invalid token!"
        return render(request, 'auth/emailverified.tpl.html', {'message' : message})


def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.tpl.html', {'profile': profile})