from django.core.management.base import BaseCommand, CommandError
from search.models import products, categories, ingredients
import requests, unicodedata

class Command(BaseCommand):

    def read_values_op_fo_fa(self):
        """Read the API data."""
        categories = [
                    "boissons",
                    "fruits-et-produits-derives",
                    "legumes-et-derives",
                    "viandes",
                    "poissons",
                    "sauces",
                    "produits-laitiers"
                    ]
        params_get = {
                    "action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "page_size": "1000",
                    "json": "1"
                }
        for values in categories:
            params_get["tag_0"] = values
            read = requests.get(
                            'https://world.openfoodfacts.org/cgi/search.pl',
                            params=params_get
                            )
            data = read.json()
            self.data_sorting(data, values)

    def data_sorting(self, data, values):
        columns = ("id",
                   "product_name_fr",
                   "generic_name_fr",
                   "ingredients_text_with_allergens_fr",
                   "nutrition_grade_fr",
                   "categories",
                   "last_edit_dates_tags",
                   "url")
        for d in data["products"]:
            product_data = []
            not_ok = False
            for c in columns:
                if c in d.keys():
                    if not d.get(c):
                        not_ok = True
                        break
                    else:
                        product_data.append(d.get(c))
            product_data.insert(1, values)
            if not_ok is False and len(product_data) == 9:
                product_data[7] = product_data[7][0]
                self.insert_data(product_data)
    
    def formating_data(self, data):
        """Allow the formatting of the data."""
        data = unicodedata.normalize('NFKD', data)\
            .encode('ASCII', 'ignore').decode()
        data = data.lower()
        data = data.replace("<span class=\"allergen\">", "")
        data = data.replace("</span>", "")
        data = data.replace("&quot", "")
        data = data.replace("&lt", "")
        data = ''.join([x if x.isalpha() else " " for x in data]).split()
        data_list = []
        for word in data:
            if len(word) > 3:
                data_list.append(word)
        return data_list


    def insert_data(self,recv):
        list_cat = self.formating_data(recv.pop(6))
        list_ing = self.formating_data(recv.pop(4))
        if products.objects.filter(id=recv[0]).exists():
            print("le produit existe déjà")
        else:
            produit=products(id=recv[0], categorie=recv[1], nom=recv[2], description=recv[3], indice=recv[4], date_update=recv[5], url=recv[6])
            produit.save()
        for cat in list_cat:
            if categories.objects.filter(name=cat).exists():
                categorie = categories.objects.get(name=cat)
                try:
                    categorie.product.add(produit)
                except:
                    print("une relation existe déjà")
            else:
                categorie = categories(name=cat)
                categorie.save()
                categorie.product.add(produit)
    
        for ing in list_ing:
            if ingredients.objects.filter(name=ing).exists():
                ingredient = ingredients.objects.get(name=ing)
                try:
                    ingredient.product.add(produit)
                except:
                    print("une relation existe déjà")
            else:
                ingredient = ingredients(name=ing)
                ingredient.save()
                ingredient.product.add(produit)
    
    def handle(self, *args, **options):
        self.read_values_op_fo_fa()
            
 