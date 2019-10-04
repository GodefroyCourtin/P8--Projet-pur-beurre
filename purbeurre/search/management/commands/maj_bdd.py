"""Allow the openfoodfact database to be updated."""
from django.core.management.base import BaseCommand
from django.conf import settings
from search.models import Product,\
    Main_categorie,\
    Sub_categorie,\
    Ingredient,\
    Nutriment
import requests
import unicodedata


class Command(BaseCommand):
    """Contains the commands used to update the database."""

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
                        "tag_0": main_categorie[0]
                    }
            read = requests.get(
                            'https://world.openfoodfacts.org/cgi/search.pl',
                            params=params_get
                            )
            raw_data = read.json()
            self.data_sorting(raw_data, main_categorie[0])

    def data_sorting(self, raw_data, main_categorie):
        """Allow sorting on the received data."""
        columns = ("id",
                   "product_name_fr",
                   "generic_name_fr",
                   "ingredients_text_with_allergens_fr",
                   "nutrition_grade_fr",
                   "categories",
                   "last_edit_dates_tags",
                   "url",
                   "image_url",
                   "nutriments")
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
            if not_ok is False and len(product_data) == 11:
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

    def sorting_nutriment(self, nutriment):
        """Allow sorting on the nutriment."""
        nutriment_data = {}
        rename_nut = {
            'fat_100g': 'Matières grasses',
            'sugars_100g': 'Sucres',
            'saturated-fat_100g': 'Acides gras saturés',
            'salt_100g': 'Sel'
        }
        for name, quantity in nutriment.items():
            for name_en, name_fr in rename_nut.items():
                if name == name_en:
                    nutriment_data[name_fr] = quantity
        return nutriment_data

    def insert_data(self, receiv_data):
        """Insert the data after sorting in the database."""
        list_sub_cat = self.formating_data(receiv_data.pop(6))
        list_ing = self.formating_data(receiv_data.pop(4))
        sorting_nutriment = self.sorting_nutriment(receiv_data.pop(8))

        if Product.objects.filter(id=receiv_data[0]).exists() is False:
            # ici on creer le produit car l'id n'existe pas
            produit = Product(
                id=receiv_data[0],
                main_categorie=receiv_data[1],
                nom=receiv_data[2],
                description=receiv_data[3],
                indice=receiv_data[4],
                date_update=receiv_data[5],
                url=receiv_data[6],
                url_img=receiv_data[7])
            produit.save()
        else:
            # ici on récupère le produit car il existe
            produit = Product.objects.get(id=receiv_data[0])

        for name, quantity in sorting_nutriment.items():
            nutriment = Nutriment.objects.get_or_create(
                nutriment_name=name,
                quantity=quantity
                )
            nutriment[0].product.add(produit)

        for sub_cat in list_sub_cat:
            sub_categorie = Sub_categorie.objects.get_or_create(
                name=sub_cat
            )
            if Sub_categorie.objects.filter(
              name=sub_cat,
              product__id=receiv_data[0]
              ).exists() is False:
                sub_categorie[0].product.add(produit)

        for ing in list_ing:
            ingredient = Ingredient.objects.get_or_create(
                name=ing
            )
            if Ingredient.objects.filter(
              name=ing,
              product__id=receiv_data[0]
              ).exists() is False:
                ingredient[0].product.add(produit)

    def handle(self, *args, **options):
        """Command that is run when running the database update."""
        self.read_values_op_fo_fa()
