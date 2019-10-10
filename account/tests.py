from django.test import TestCase
from .models import My_user, Substitute
from search.models import Main_categorie, Product


class SignupPageTestCase(TestCase):
    def test_signup(self):
        response = self.client.get('/account/sign_up')
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        response = self.client.post('/account/sign_up', {
            'username': 'cyril',
            'last_name': 'Simonin',
            'first_name': 'cyril',
            'email': 'monemail@emil.fr',
            'password': 'my_password'
            })
        self.assertEqual(response.status_code, 200)


class SigninPageTestCase(TestCase):
    def setUp(self):
        user = My_user.objects.create_user(
            "cyril",
            "cyril@email.fr",
            "my_password"
            )
        user.last_name = "simonin"
        user.first_name = "cyril"
        user.save()

    def test_signin(self):
        response = self.client.get('/account/sign_in')
        self.assertEqual(response.status_code, 200)

    def test_signin_post(self):
        response = self.client.post('/account/sign_in', {
            'username': 'cyril',
            'password': 'my_password'
            })
        self.assertEqual(response.status_code, 302)


class favoritePageTestCase(TestCase):
    def setUp(self):
        user = My_user.objects.create_user(
            "cyril",
            "cyril@email.fr",
            "my_password"
            )
        user.last_name = "simonin"
        user.first_name = "cyril"
        user.save()

        main_categorie = Main_categorie.objects.create(name="boisson")
        produit1 = Product(
                id=5449000000996,
                main_categorie=main_categorie,
                nom="coca",
                indice="e",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        produit1.save()

        produit2 = Product(
                id=5449000133335,
                main_categorie=main_categorie,
                nom="Coca Cola Zero",
                indice="e",
                url="http://url.fr/openfoodfact",
                url_img="http://url.fr/openfoodfact/image")
        produit2.save()

        Substitute.objects.create(
            product_initial=produit1,
            product_substitute=produit2,
            myuser=user)

        self.client.login(username="cyril", password="my_password")

    def test_view_favorite(self):
        response = self.client.get('/account/favorite')
        self.assertEqual(response.status_code, 200)

    def test_remove_favorite(self):
        response = self.client.get(
            '/account/remove_favorite/5449000000996/5449000133335/'
            )
        self.assertEqual(response.status_code, 302)


class SignoutPageTestCase(TestCase):
    def setUp(self):
        user = My_user.objects.create_user(
            "cyril",
            "cyril@email.fr",
            "my_password"
            )
        user.last_name = "simonin"
        user.first_name = "cyril"
        user.save()
        self.client.login(username="cyril", password="my_password")

    def test_signout(self):
        response = self.client.get('/account/sign_out')
        self.assertEqual(response.status_code, 302)


class MyaccountTestCase(TestCase):
    def setUp(self):
        user = My_user.objects.create_user(
            "cyril",
            "cyril@email.fr",
            "my_password"
            )
        user.last_name = "simonin"
        user.first_name = "cyril"
        user.save()
        self.client.login(username="cyril", password="my_password")

    def test_myaccount(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
