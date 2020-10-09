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
        request = requests.get(category[2] + ".json")
        products = request.json()["products"]
        return products


    def fill_database(self) -> None:
        """
        This function initiates the database with all the data needed
        :return: None
        """
        categories = OpenApi().get_categories()
        for category in categories:
            name = "'" + category["name"].replace("'", "\\'") + "'"
            url = "'" + category["url"] + "'"
            if not Category.objects.get(name=name):
                Category.objects.create(name=name, url=url)
        categories = Category.objects.all()
        for category in categories:
            aliments = OpenApi().get_aliments(category)
            for aliment in aliments:
                headers = ["product_name", "category", "nutrition_grades", "stores"]
                aliment["category"] = category[0]
                data = {}
                for header in headers:
                    try:
                        data[header] = aliment[header]
                        # data.append("'" + aliment[header].replace("'", "\\'") + "'")
                    except KeyError:
                        data[header] = None
                Aliment.objects.create(**data)
