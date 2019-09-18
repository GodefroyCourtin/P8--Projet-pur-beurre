from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render

from .models import Product, Main_categorie, Sub_categorie, Ingredient
from .forms import search

def index(request):
    return render(request, 'search/index.html', {'form': search()})

def result(request):
    if request.method == 'POST':
        form = search(request.POST)
        if form.is_valid():
            name_prod = form.cleaned_data['search_prod']
            search_prod = Product.objects.filter(nom__icontains=name_prod)
            return render(request, 'search/result.html',{'product_list': search_prod})


def detail(request, product_id):
    detail_product = get_object_or_404(Product, id=product_id) #recupération des information sur le produit
    info_prod = {
        'detail_product': detail_product,
        'ingredient': Ingredient.objects.filter(product=product_id)
    }
    return render(request, 'search/detail.html', info_prod)