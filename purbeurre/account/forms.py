from django import forms

class Signup(forms.Form):
    username = forms.CharField(label='Nom d\'utilsiateur', max_length=25)
    last_name = forms.CharField(label='Nom',max_length=30)
    first_name = forms.CharField(label='Prénom',max_length=30)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Mot de passe',min_length=8, widget=forms.PasswordInput())

class Signin(forms.Form):
    username = forms.CharField(label='Nom d\'utilsiateur',max_length=25)
    password = forms.CharField(label='Mot de passe',min_length=8, widget=forms.PasswordInput())

class ChangePassword(forms.Form):
    password = forms.CharField(label='Mot de passe',min_length=8, widget=forms.PasswordInput())

class ChangeEmail(forms.Form):
    email = forms.EmailField(label='Email')



