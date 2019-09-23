from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from search.models import Product, Main_categorie, Sub_categorie, Ingredient
import requests, unicodedata

class Command(BaseCommand):

    def read_values_op_fo_fa(self):
        """Read the API data."""
        for cat in settings.MAIN_CATEGORIE:
            main_categorie = Main_categorie.objects.update_or_create(
                    name=cat
                )
            params_get = {
                        "action": "process",
                        "tagtype_0": "categories",
                        "tag_contains_0": "contains",
                        "page_size": "1000",
                        "json": "1",
                        "tag_0":main_categorie[0]
                    }
            read = requests.get(
                            'https://world.openfoodfacts.org/cgi/search.pl',
                            params=params_get
                            )
            raw_data = read.json()
            self.data_sorting(raw_data, main_categorie[0])

    def data_sorting(self, raw_data, main_categorie):
        columns = ("id",
                   "product_name_fr",
                   "generic_name_fr",
                   "ingredients_text_with_allergens_fr",
                   "nutrition_grade_fr",
                   "categories",
                   "last_edit_dates_tags",
                   "url")
        for data in raw_data["products"]:
            product_data = []
            not_ok = False
            for num_col in columns:
                if num_col in data.keys():
                    if not data.get(num_col):
                        not_ok = True
                        break
                    else:
                        product_data.append(data.get(num_col))
            product_data.insert(1, main_categorie)
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


    def insert_data(self,receiv_data):
        list_sub_cat = self.formating_data(receiv_data.pop(6))
        list_ing = self.formating_data(receiv_data.pop(4))

        '''La fonction get_or_create de django ne sera pas utilisé car celle-ci verifie l'égalité de tous les champs
        l'API OPEN FOOD FACT renvoi certain produit avec le meme ID mais pas les mêmes descriptions ce qui a pour effet 
        de faire planter la fonction get_or_create puisque l'id est unique dans la BDD'''
        if Product.objects.filter(id=receiv_data[0]).exists() is False:
            #ici on creer le produit car l'id n'existe pas
            produit=Product(
                id=receiv_data[0],
                categorie=receiv_data[1],
                nom=receiv_data[2],
                description=receiv_data[3],
                indice=receiv_data[4],
                date_update=receiv_data[5],
                url=receiv_data[6])
            produit.save()
        else:
            #ici on récupère le produit car il existe
            produit=Product.objects.get(id=receiv_data[0])

        for sub_cat in list_sub_cat:
            sub_categorie = Sub_categorie.objects.get_or_create(
                name=sub_cat
            )
            if Sub_categorie.objects.filter(name=sub_cat, product__id=receiv_data[0]).exists() is False:
                sub_categorie[0].product.add(produit)

        for ing in list_ing:
            ingredient = Ingredient.objects.get_or_create(
                name=ing
            )
            if Ingredient.objects.filter(name=ing, product__id=receiv_data[0]).exists() is False:
                ingredient[0].product.add(produit)
    
    def handle(self, *args, **options):
        self.read_values_op_fo_fa()
            
 