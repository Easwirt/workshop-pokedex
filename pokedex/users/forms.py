from django import forms
from .models import Profile
from django.contrib.auth.password_validation import validate_password

class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}), help_text="Your password can't be too similar to your other personal information, must contain at least 8 characters, and can't be entirely numeric.", validators=[validate_password])
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except forms.ValidationError as error:
            self.add_error('password', error)
        return password
    


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
