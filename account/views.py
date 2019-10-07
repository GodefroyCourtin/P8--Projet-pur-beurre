"""Contains function used for views app account."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import Signin, Signup
from .models import My_user, Substitute
from search.models import Product, Nutriment
from django.contrib.auth.decorators import login_required


def sign_up(request):
    """Display the sign up form."""
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = My_user.objects.create_user(username, email, password)
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.save()
            context = {
                "username": username
            }
            return render(request, 'account/signup.html', context)
    else:
        return render(request, 'account/signup.html', {'form': Signup()})


def sign_in(request):
    """Display the sign in form."""
    if request.method == 'POST':
        form = Signin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(
                    request,
                    'account/signin.html',
                    {'form': Signin()}
                    )
    else:
        return render(request, 'account/signin.html', {'form': Signin()})


@login_required
def favorite(request):
    """Display the user’s favorites."""
    product_list = Substitute.objects.filter(myuser=request.user)
    context = {
        "products_list": []
    }
    for line in product_list:
        context["products_list"].append([
                (
                    line.product_initial,
                    Nutriment.objects.filter(product=line.product_initial)
                    ),
                (
                    line.product_substitute,
                    Nutriment.objects.filter(product=line.product_substitute)
                    )
                ])
    return render(request, 'account/favorite.html', context)


@login_required
def remove_favorite(request, product_id, product_id_replacement):
    """Allow the user to delete a favorites."""
    user = My_user.objects.get(id=request.user.id)
    product_initial = Product.objects.get(id=product_id)
    product_substitute = Product.objects.get(id=product_id_replacement)
    search = get_object_or_404(
        Substitute,
        myuser=user,
        product_initial=product_initial,
        product_substitute=product_substitute
        )
    search.delete()
    return redirect('/account/favorite')


@login_required
def sign_out(request):
    """Allow the user to disconnect."""
    logout(request)
    return redirect('/')


@login_required
def my_account(request):
    """Allow the user to view their account information."""
    user = My_user.objects.get(id=request.user.id)
    return render(request, 'account/my_account.html', {'account': user})
