from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=100)
