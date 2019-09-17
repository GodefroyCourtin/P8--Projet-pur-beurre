from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render

from .models import products, categories, ingredients
from .forms import search

def index(request):
    print(request.POST)
    if request.method == 'POST':
        form = search(request.POST)
        if form.is_valid():
            # search_prod = form.cleaned_data['search_prod'] < a quoi ser cleaned DATA
            return render(request, 'search/result.html')
    else:
        form = search()
    return render(request, 'search/index.html', {'form': form})

def result(request):
    list_all_products = products.objects.filter(nom__icontains=request.POST["search_prod"])
    # list_all_products = products.objects.order_by('id')
    context = {'product_list': list_all_products}
    return render(request, 'search/result.html', context)

def detail(request, product_id):
    detail_product = get_object_or_404(products, id=product_id) #recupération des information sur le produit
    info_prod = {
        'detail_product': detail_product,
        'ingredient': ingredients.objects.filter(product=product_id)
    }
    return render(request, 'search/detail.html', info_prod)