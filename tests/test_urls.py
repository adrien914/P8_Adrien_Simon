from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from main.views import index, mentions, search_substitutes, show_aliment_info, show_saved_substitutes
from main.views import save_substitute, delete_substitute, register

# Create your tests here.


class TestUrl(SimpleTestCase):
    """Calss used to test the uls"""

    def test_index_is_resolved(self):
        url = reverse("main:index")
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_mentions_is_resolved(self):
        url = reverse("main:mentions")
        print(resolve(url))
        self.assertEquals(resolve(url).func, mentions)

    def test_search_substitutes_is_resolved(self):
        url = reverse("main:search_substitutes")
        print(resolve(url))
        self.assertEquals(resolve(url).func, search_substitutes)

    def test_show_aliment_info_is_resolved(self):
        url = reverse("main:show_aliment_info", args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, show_aliment_info)

    def test_show_saved_substitutes_is_resolved(self):
        url = reverse("main:show_saved_substitutes")
        print(resolve(url))
        self.assertEquals(resolve(url).func, show_saved_substitutes)

    def test_save_substitute_is_resolved(self):
        url = reverse("main:save_substitute", args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, save_substitute)

    def test_delete_substitute_is_resolved(self):
        url = reverse("main:delete_substitute", args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, delete_substitute)



    def test_register_is_resolved(self):
        url = reverse("main:register")
        print(resolve(url))
        self.assertEquals(resolve(url).func, register)
