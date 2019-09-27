from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import Signin, Signup, ChangePassword, ChangeEmail
from .models import My_user, Substitute
from search.models import Product
from django.contrib.auth.decorators import login_required

def sign_up(request):
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

@login_required
def sign_out(request):
    logout(request)
    return render(request, 'account/sign_out.html')

@login_required
def modif_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            user = My_user.objects.get(id=request.user.id)
            user.set_password(form.cleaned_data['password'])
            user.save()
            context={
                "password_changed": "Votre mot de pass à été changer."
            }
            return render(request, 'account/password.html',context)
    else:
        return render(request, 'account/password.html',{'form': ChangePassword()})

@login_required
def modif_email(request):
    if request.method == 'POST':
        form = ChangeEmail(request.POST)
        if form.is_valid():
            user = request.user
            user.email= form.cleaned_data['email']
            user.save()
            context={
                "email_changed": "Votre email à été changer."
            }
            return render(request, 'account/email.html',context)
    else:
        return render(request, 'account/email.html',{'form': ChangeEmail()})

@login_required
def favorite(request):
    user = My_user.objects.get(id=request.user.id)
    product_list = Substitute.objects.filter(myuser=request.user)
    context = {
        "products_list":[]
    }
    for line in product_list:
        context["products_list"].append([line.product_initial, line.product_substitute])

    return render(request, 'account/favorite.html', context)

@login_required
def remove_favorite(request, product_id, product_id_replacement):
    user = My_user.objects.get(id=request.user.id)
    product_initial = Product.objects.get(id=product_id)
    product_substitute=Product.objects.get(id=product_id_replacement)
    try:
        Substitute.objects.get(myuser=user, product_initial=product_initial, product_substitute =product_substitute).delete()
        context ={
            "relation": "Exist",
            "delete_initial":product_initial,
            "delete_substitute":product_substitute
        }

    except Substitute.DoesNotExist:
         context ={
            "delete_initial":product_initial,
            "delete_substitute":product_substitute
        }
    return render(request,'account/remove_favorite.html', context)

@login_required
def delete_account(request):
    user = My_user.objects.get(id=request.user.id)
    user.delete()
    return render(request, 'account/delete_account.html')