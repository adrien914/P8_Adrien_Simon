from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from main.models import Aliment, Substitute, Category
from django.contrib.auth.models import User


class TestIndex(TestCase):

    def setUp(self):
        self.client = Client()
        self.index = reverse('main:index')

    def test_homepage_GET(self):
        response = self.client.get(self.index)
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/index/zfqfzq')
        self.assertEquals(response.status_code, 404)


class TestRegister(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test", password="test")

    def test_get_register_page(self):
        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)

    def test_registration_invalid_infos(self):
        self.client.post(
            path=reverse('main:register'),
            data={'username': 'test',
                  'email': 'email',
                  'password1': '1234',
                  'password2': '12345'})
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)


class TestLogout(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test", password="test")

    def test_logout_redirect_visitor(self):
        self.client.login()
        self.client.logout()
        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.status_code, 302)

    def test_logout_view_user_status(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)


class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test", password="test")

    def test_access_login_page(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        self.client.post(reverse("main:login"), {"username": "test", "password": "test"})
        self.assertEqual(self.user.is_authenticated, True)


class TestSearchSubstitute(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            id=9999999,
            name="Jambons de jambons test",
            url="http://category.url",
        )
        self.aliment = Aliment.objects.create(
            id=9999999,
            url="http://url.url",
            product_name="Jambon de jambon",
            nutrition_grades="b",
            stores="Leclerc",
            image_url="http://image_url.url",
            category=self.category,
        )
        for i in range(1, 11):
            Aliment.objects.create(
                id=9999999 + i,
                url="http://url.url",
                product_name="Jambon de jambon " + str(i),
                nutrition_grades="b",
                stores="Leclerc",
                image_url="http://image_url.url",
                category=self.category,
            )

    def test_search_substitute_get_view(self):
        response = self.client.get(reverse("main:search_substitutes"), {"aliment_search": "jambon"})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("main:search_substitutes"), args="non")
        self.assertEqual(response.status_code, 200)

    def test_search_substitute_pagination_page_1(self):
        response = self.client.get(reverse("main:search_substitutes"), {"aliment_search": "jambon"})
        self.assertEqual(response.status_code, 200)
        content = response.content()
        self.assertIn("Suivant", content)
        self.assertNotIn("Précédent", content)

    def test_search_substitute_pagination_page_2(self):
        response = self.client.get(reverse("main:search_substitutes"), {"aliment_search": "jambon", "page": 2})
        self.assertEqual(response.status_code, 200)
        content = response.content()
        self.assertNotIn("Suivant", content)
        self.assertIn("Précédent", content)

class TestPasswordChange(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test", password="test")

    def test_password_change_is_logged_in(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("main:password_change"))
        self.assertEqual(response.status_code, 302)

    def test_password_change_visitor(self):
        self.client = Client()
        self.client.logout()
        response = self.client.get(reverse("main:password_change"))
        self.assertRedirects(response, "/accounts/login/?next=/password_change/")


class TestShowAlimentInfo(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            id=9999999,
            name="Jambons de jambons test",
            url="http://category.url",
        )
        self.aliment = Aliment.objects.create(
            id=9999999,
            url="http://url.url",
            product_name="Jambon de jambon",
            nutrition_grades="b",
            stores="Leclerc",
            image_url="http://image_url.url",
            category=self.category,
        )

    def test_aliment_info_valid_page(self):
        response = self.client.get('/aliment_info/' + str(self.aliment.id))
        self.assertEqual(response.status_code, 301)

    def test_aliment_info_empty_args(self):
        response = self.client.get('/aliment_info/')
        self.assertEqual(response.status_code, 404)

    def test_aliment_info_wrong_args(self):
        response = self.client.get('/aliment_info/test/')
        self.assertEqual(response.status_code, 404)


class TestSaveSubstitute(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test", password="test")
        self.category = Category.objects.create(
            id=9999999,
            name="Jambons de jambons test",
            url="http://category.url",
        )
        self.aliment = Aliment.objects.create(
            id=9999999,
            url="http://url.url",
            product_name="Jambon de jambon",
            nutrition_grades="b",
            stores="Leclerc",
            image_url="http://image_url.url",
            category=self.category,
        )

    def test_save_aliment_view(self):
        self.client.login(username='test', password='test')
        substitute = Substitute.objects.create(
            id=1,
            product_name=self.aliment.product_name,
            category=self.category,
            user=self.user,
            aliment=self.aliment
        )
        substitute = Substitute.objects.get(id=1)
        self.assertTrue(substitute)


class TestDeleteSubstitute(TestCase):
    '''Calss used to test the delete view'''

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test", password="test")
        self.category = Category.objects.create(
            id=9999999,
            name="Jambons de jambons test",
            url="http://category.url",
        )
        self.aliment = Aliment.objects.create(
            id=9999999,
            url="http://url.url",
            product_name="Jambon de jambon",
            nutrition_grades="b",
            stores="Leclerc",
            image_url="http://image_url.url",
            category=self.category,
        )
        self.substitute = Substitute.objects.create(
            id=1,
            product_name=self.aliment.product_name,
            category=self.category,
            user=self.user,
            aliment=self.aliment
        )

    def test_delete_logged_in(self):
        self.client.login(username='test', password='test')
        response = self.client.get("/delete_substitute/" + str(self.substitute.id))
        self.assertEqual(response.status_code, 301)

    def test_delete_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/delete_substitute/" + str(self.substitute.id))
        self.assertEqual(response.status_code, 301)
