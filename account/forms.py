"""Module containing the different forms for the account application."""
from django import forms


class Signup(forms.Form):
    """Contain the registration form."""

    username = forms.CharField(label='Nom d\'utilsiateur', max_length=25)
    last_name = forms.CharField(label='Nom', max_length=30)
    first_name = forms.CharField(label='Prénom', max_length=30)
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Mot de passe',
        min_length=8,
        widget=forms.PasswordInput()
        )


class Signin(forms.Form):
    """Contain the authentication form."""

    username = forms.CharField(label='Nom d\'utilsiateur', max_length=25)
    password = forms.CharField(
        label='Mot de passe',
        min_length=8,
        widget=forms.PasswordInput()
        )
