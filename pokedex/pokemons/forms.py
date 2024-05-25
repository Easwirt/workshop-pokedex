from django import forms

class SearchForm(forms.Form):
    query = forms.CharField()

class PurchasePokemonForm(forms.Form):
    pokemon_id = forms.IntegerField(widget=forms.HiddenInput())


class SellPokemonForm(forms.Form):
    pokemon_id = forms.IntegerField(widget=forms.HiddenInput())