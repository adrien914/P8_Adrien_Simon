from main.models import Aliment, Category, Substitute
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class ModelsTestCase(TestCase):
    def setUp(self) -> None:
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
            id=9999999,
            url="http://url.url",
            product_name="Jambon de jambon mieux",
            nutrition_grades="a",
            stores="Leclerc",
            image_url="http://image_url.url",
            category=self.category,
            aliment=self.aliment,
            user=self.user,
        )

    def test_aliment_valid(self):
        self.assertEqual(self.aliment.product_name, "Jambon de jambon")
        self.assertEqual(self.aliment.nutrition_grades, "b")
        self.assertNotEqual(self.aliment.product_name, "Pas produit")

    def test_aliment_no_duplicate(self):
        self.assertRaises(
            IntegrityError,
            lambda: Aliment.objects.create(
                id=9999998,
                product_name="Jambon de jambon",
                category=self.category,
            )
        )

    def test_substitute_valid(self):
        self.assertEqual(self.substitute.product_name, "Jambon de jambon mieux")
        self.assertEqual(self.substitute.nutrition_grades, "a")
        self.assertNotEqual(self.substitute.product_name, "Pas produit")

    def test_substitute_duplicates(self):
        try:
            Substitute.objects.create(
                id=9999998,
                product_name="Jambon de jambon",
                aliment=self.aliment,
                category=self.category,
                user=self.user,
            )
        except IntegrityError:
            self.fail()
