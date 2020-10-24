import requests
from main.models import Category, Aliment, Substitute


class OpenApi:

    @staticmethod
    def get_categories() -> list:
        """
        Get a certain number of categories from the openfooodfacts api
        :return: the list of the categories retrieved from the api
        """
        request = requests.get("https://fr.openfoodfacts.org/categories.json")
        if request.status_code != 200:
            raise Exception("Il y a eu un problème avec la connexion a l'api OpenFoodFacts "
                            "veuillez reessayer plus tard")
        categories = request.json()["tags"][:10]
        return categories

    @staticmethod
    def get_aliments(category):
        """
        Get a certain number of aliments from a category from the openfoodfacts api
        :param category: the category to retrieve the aliments from
        :return: the aliments retrieved from the api
        """
        print(str(category.url) + ".json")
        request = requests.get(category.url + ".json")
        products = request.json()["products"]
        return products


    def fill_database(self) -> None:
        """
        This function initiates the database with all the data needed
        :return: None
        """
        print(Category.objects.all())
        print()
        categories = OpenApi().get_categories()
        for category in categories:
            name = category["name"]
            url = category["url"]
            if not Category.objects.filter(name=name):
                Category.objects.create(name=name, url=url)
        categories = Category.objects.all()
        for category in categories:
            aliments = OpenApi().get_aliments(category)
            for aliment in aliments:
                print(aliment)
                headers = ["product_name", "category", "nutrition_grades", "stores", "image_url", "url"]
                aliment["category"] = category
                data = {}
                for header in headers:
                    try:
                        data[header] = aliment[header]
                    except KeyError:
                        data[header] = None
                try:
                    Aliment.objects.create(**data)
                except:
                    data["product_name"] += " - " + str(len(Aliment.objects.filter(product_name__contains=data["product_name"])))
                    print(data["product_name"])
                    Aliment.objects.create(**data)
