"""Contains function used for views app search."""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .models import Product, Ingredient, Nutriment
from account.models import My_user, Substitute
from .forms import search


def index(request):
    """Display the site index."""
    return render(request, 'search/index.html', {'form': search()})


def result(request):
    """Display the search result."""
    if request.method == 'POST':
        form = search(request.POST)
        if form.is_valid():
            name_prod = form.cleaned_data['search_prod']
            search_prod = Product.objects.filter(nom__search=name_prod)
            context = {
                'product_list': search_prod,
                'search_prod': name_prod
                }
            return render(request, 'search/result.html', context)
    else:
        raise Http404


def detail(request, product_id):
    """Display the detail product with substitution product."""
    detail_product = get_object_or_404(Product, id=product_id)
    substitute = detail_product.compare_search()
    info_prod = {
        'detail_product': detail_product,
        'nutriment': Nutriment.objects.filter(product=product_id),
        'ingredient': Ingredient.objects.filter(product=product_id),
        'substitute': substitute
    }
    return render(request, 'search/detail.html', info_prod)


def save(request, product_id, product_id_replacement):
    """Save product in favorites."""
    if request.user.is_authenticated:
        user = get_object_or_404(
            My_user,
            id=request.user.id
            )
        product_initial = get_object_or_404(
            Product,
            id=product_id
            )
        product_substitute = get_object_or_404(
            Product,
            id=product_id_replacement
            )
        Substitute.objects.update_or_create(
            product_initial=product_initial,
            product_substitute=product_substitute,
            myuser=user)
        return redirect('account:favorite')
    else:
        return redirect('account:sign_up')


def mentions_legal(request):
    """Display the legal mentions of the site."""
    return render(request, 'search/mentions_legal.html')
