"""Django administration module."""
from django.contrib import admin
from .models import Product, Main_categorie, Sub_categorie, Ingredient
admin.site.register(Product)
admin.site.register(Main_categorie)
admin.site.register(Sub_categorie)
admin.site.register(Ingredient)
