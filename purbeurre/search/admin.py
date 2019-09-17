from django.contrib import admin
from .models import products, categories, ingredients, product_save
admin.site.register(products)
admin.site.register(categories)
admin.site.register(ingredients)
admin.site.register(product_save)
