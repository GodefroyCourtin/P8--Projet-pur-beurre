"""Module containing the different forms for the search application."""
from django import forms


class search(forms.Form):
    """Contain the search form."""
    search_prod = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Produit','class': 'rounded'}))

