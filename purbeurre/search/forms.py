from django import forms

class search(forms.Form):
    search_prod = forms.CharField(label='Votre recherche', max_length=100)