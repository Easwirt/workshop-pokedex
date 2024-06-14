from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .tokens import email_verification_token
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from pokedex.settings import DEFAULT_URL
from .models import User, EmailVerificationToken
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            

            if User.objects.filter(username=username).exists():
                message = "Username already exists! Please try a different username."
                form.add_error('username', message)
                return render(request, 'auth/signup.tpl.html', {'form': form})


            
            if User.objects.filter(email=email).exists():
                message = "Email already registered!"
                form.add_error('email', message)
                return render(request, 'auth/signup.tpl.html', {'form': form})

            

            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
        
            verification_token = email_verification_token.make_token(user)
            EmailVerificationToken.objects.create(user=user, token=verification_token)
            verification_link = f'{DEFAULT_URL}/auth/emailverification/{urlsafe_base64_encode(force_bytes(user.pk))}/{verification_token}'
            
            subject = "Please verify your email address..."
            message = f"Hello {user.username},\n\nPlease click on the link below to verify your email address:\n\n{verification_link}"
            email = EmailMessage(subject, message, to=[email])
            email.send()
            message = "Please check your email for verification mail."
            success_message = "Please check your email for verification."
            messages.success(request, success_message)
            return render(request, 'auth/signup.tpl.html', {'form': form, 'success_message' : success_message})
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.tpl.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile/')
            else:
                message = "Invalid username or password"
                form.add_error('username', message)
                return render(request, 'auth/login.tpl.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'auth/login.tpl.html', {'form': form})

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
        user.email_confirmed = True
        user.save()
        login(request, user)
        token_obj.delete()
        message = "Your email has been verified."
        return render(request, 'auth/emailverified.tpl.html', {'message' : message})
    else:
        message = "Invalid token!"
        token_obj.delete()
        return render(request, 'auth/emailverified.tpl.html', {'message' : message})