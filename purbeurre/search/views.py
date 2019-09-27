from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render

from .models import Product, Main_categorie, Sub_categorie, Ingredient
from account.models import My_user, Substitute
from .forms import search

def index(request):
    return render(request, 'search/index.html', {'form': search()})

def result(request):
    if request.method == 'POST':
        form = search(request.POST)
        if form.is_valid():
            name_prod = form.cleaned_data['search_prod']
            search_prod = Product.objects.filter(nom__search=name_prod)
            return render(request, 'search/result.html',{'product_list': search_prod})

def detail(request, product_id):
    detail_product = get_object_or_404(Product, id=product_id)
    info_prod = {
        'detail_product': detail_product,
        'ingredient': Ingredient.objects.filter(product=product_id)
    }
    return render(request, 'search/detail.html', info_prod)

def substitute(request, product_id):
    detail_product = get_object_or_404(Product, id=product_id)
    result=detail_product.compare_search()
    result["id_primary_product"] = product_id
    return render(request, 'search/substitute.html',result)

def save(request, product_id, product_id_replacement):
    if request.user.is_authenticated:
        user = My_user.objects.get(id=request.user.id)
        product_initial=Product.objects.get(id=product_id)
        product_substitute=Product.objects.get(id=product_id_replacement)
        Substitute.objects.update_or_create(product_initial=product_initial, product_substitute=product_substitute, myuser=user)
    else:
        print("nop")
    return render(request, 'search/save.html')
    