from django.test import TestCase
from .models import Main_categorie, Product
from account.models import My_user


# Test view
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ResultPageTestCase(TestCase):
    def test_result_page(self):
        response = self.client.get('/result/')
        self.assertEqual(response.status_code, 404)

    def test_result_page_ok(self):
        response = self.client.post('/result/', {'search_prod': 'coca'})
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):
    def setUp(self):
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

    def test_detail_page_not_found(self):
        response = self.client.get('/1945/')
        self.assertEqual(response.status_code, 404)

    def test_detail_page_found(self):
        response = self.client.get('/5449000000996/')
        self.assertEqual(response.status_code, 200)


class SavePageTestCase(TestCase):
    def setUp(self):
        main_categorie = Main_categorie.objects.create(name="boisson")
        produit1 = Product(
                id=5449000000996,
                main_categorie=main_categorie,
                nom="coca",
                description="une description",
                indice="e",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        produit1.save()

        produit2 = Product(
                id=5449000133335,
                main_categorie=main_categorie,
                nom="Coca Cola Zero",
                description="une description",
                indice="e",
                date_update="2019-10-12",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        produit2.save()

        user = My_user.objects.create_user(
            "cyril",
            "cyril@email.fr",
            "password"
            )
        user.last_name = "simonin"
        user.first_name = "cyril"
        user.save()
        self.client.login(username="cyril", password="password")

    def test_save_page_not_found(self):
        response = self.client.get('/save/1945/1945/')
        self.assertEqual(response.status_code, 404)

    def test_save_page_found(self):
        response = self.client.get('/save/5449000000996/5449000133335/')
        self.assertEqual(response.status_code, 302)

    def test_save_page_not_found_not_authentificated(self):
        self.client.logout()
        response = self.client.get('/save/5449000000996/5449000133335/')
        self.assertEqual(response.status_code, 302)


class MentionsLegalTestCase(TestCase):
    def test_mentions_legale_found(self):
        response = self.client.get('/mentions_legal/')
        self.assertEqual(response.status_code, 200)
