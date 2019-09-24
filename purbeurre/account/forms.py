from django import forms

class Signup(forms.Form):
    username = forms.CharField(label='Nom d\'utilsiateur', max_length=25)
    last_name = forms.CharField(label='Nom',max_length=30)
    first_name = forms.CharField(label='Prénom',max_length=30)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Mot de passe',min_length=8, widget=forms.PasswordInput())
    street_number=forms.IntegerField(label='Numero de rue')
    street=forms.CharField(label='Rue', max_length=500)
    postal_code=forms.IntegerField(label='Code postale')
    city=forms.CharField(label='Ville', max_length=20)

class Signin(forms.Form):
    username = forms.CharField(label='Nom d\'utilsiateur',max_length=25)
    password = forms.CharField(label='Mot de passe',min_length=8, widget=forms.PasswordInput())
