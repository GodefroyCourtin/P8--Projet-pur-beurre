from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import Signin, Signup
from .models import User

def sign_up(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)

            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.street_number=form.cleaned_data['street_number']
            user.street=form.cleaned_data['street']
            user.postal_code=form.cleaned_data['postal_code']
            user.city=form.cleaned_data['city']
            user.save()
            context={
                "username": username
            }
            return render(request, 'account/signup.html',context)
    else:
        return render(request, 'account/signup.html',{'form': Signup()})

def sign_in(request):
    if request.method == 'POST':
        form = Signin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                context ={
                    "username": user
                }
                return render(request, 'account/signin.html',context)
    else:
        return render(request, 'account/signin.html',{'form': Signin()})

def sign_out(request):
    logout(request)
    return render(request, 'account/sign_out.html')

# def erase(request):
