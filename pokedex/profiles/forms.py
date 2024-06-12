from django import forms


class BioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows': 3,'maxlength': 100, 'placeholder': 'Enter your bio here...'}),max_length=100,label="Bio",help_text="Maximum 100 characters.")