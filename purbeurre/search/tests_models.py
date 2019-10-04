from django.test import TestCase
from .models import Main_categorie, \
    Product, \
    Nutriment, \
    Sub_categorie, \
    Ingredient


class ProductTestCase(TestCase):
    def setUp(self):
        main_categorie = Main_categorie.objects.create(name="boisson")
        self.produit1 = Product(
                id=5449000000996,
                main_categorie=main_categorie,
                nom="coca",
                description="une description",
                indice="e",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        self.produit1.save()

        self.produit2 = Product(
                id=5449000133335,
                main_categorie=main_categorie,
                nom="Coca Cola Zero",
                description="une description",
                indice="b",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        self.produit2.save()

        name_ing = "un ingredient"
        ing = Ingredient.objects.create(name=name_ing)
        ing.product.add(self.produit1)
        ing.product.add(self.produit2)

        name_subcat = "une subcat"
        subcat = Sub_categorie.objects.create(name=name_subcat)
        subcat.product.add(self.produit1)
        subcat.product.add(self.produit2)

    def test_create_product(self):
        main_categorie = Main_categorie.objects.create(name="boisson")
        produit = Product(
                id=5449000000996,
                main_categorie=main_categorie,
                nom="coca",
                description="une description",
                indice="e",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        produit.save()
        self.assertEqual(produit.id, 5449000000996)
        self.assertEqual(produit.main_categorie, main_categorie)
        self.assertEqual(produit.description, "une description")
        self.assertEqual(produit.indice, "e")
        self.assertEqual(produit.date_update, "2019-10-12")
        self.assertEqual(produit.url, "http://url.fr/openfoodfact")
        self.assertEqual(produit.url_img, "http://url.fr/openfoodfact/image")

    def test_compare_product(self):
        test = self.produit1.compare_search()
        self.assertEqual(test["result_products"][0][0].id, 5449000133335)


class MainCategorieTestCase(TestCase):
    def test_create_Main_categorie(self):
        main_categorie = Main_categorie.objects.create(name="boisson")
        search = Main_categorie.objects.get(name="boisson")
        self.assertEqual(main_categorie, search)


class NutrimentTestCase(TestCase):
    def setUp(self):
        main_categorie = Main_categorie.objects.create(name="boisson")
        self.produit = Product(
                id=5449000000996,
                main_categorie=main_categorie,
                nom="coca",
                description="une description",
                indice="e",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        self.produit.save()

    def test_create_nutriment(self):
        name = "un nutriment"
        quantity = "5"
        nutriment = Nutriment.objects.create(
            nutriment_name=name,
            quantity=quantity
            )
        nutriment.product.add(self.produit)
        search = Nutriment.objects.get(nutriment_name=name, quantity=quantity)

        self.assertEqual(nutriment, search)
        self.assertEqual(nutriment.nutriment_name, "un nutriment")
        self.assertEqual(nutriment.quantity, "5")


class SubCatTestCase(TestCase):
    def setUp(self):
        main_categorie = Main_categorie.objects.create(name="boisson")
        self.produit = Product(
                id=5449000000996,
                main_categorie=main_categorie,
                nom="coca",
                description="une description",
                indice="e",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        self.produit.save()

    def test_create_subcat(self):
        name = "une subcat"
        subcat = Sub_categorie.objects.create(name=name)
        subcat.product.add(self.produit)
        search = Sub_categorie.objects.get(name=name)
        self.assertEqual(subcat, search)
        self.assertEqual(search.name, "une subcat")


class IngredientTestCase(TestCase):
    def setUp(self):
        main_categorie = Main_categorie.objects.create(name="boisson")
        self.produit = Product(
                id=5449000000996,
                main_categorie=main_categorie,
                nom="coca",
                description="une description",
                indice="e",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        self.produit.save()

    def test_create_ingredient(self):
        name = "un ingredient"
        ing = Ingredient.objects.create(name=name)
        ing.product.add(self.produit)
        search = Ingredient.objects.get(name=name)
        self.assertEqual(ing, search)
        self.assertEqual(search.name, "un ingredient")
