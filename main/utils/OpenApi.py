import requests

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
    def get_aliments( category):
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
        print("Récupération des catégories a partir de l'API OpenFoodFacts ...")
        categories = OpenApi().get_categories()
        print("Insertion des catégories en base de données ...")
        for category in categories:
            name = "'" + category["name"].replace("'", "\\'") + "'"
            url = "'" + category["url"] + "'"
            if not self.select("category", "name={}".format(name)):
                self.insert("category", ["name", "url"], [name, url])
        print("Terminé. Récupération des aliments pour chaque catégorie ...")
        categories = self.select("category")
        print("Insertion des aliments dans les catégorie: ...")
        for category in categories:
            aliments = OpenApi().get_aliments(category)
            for aliment in aliments:
                headers = ["product_name", "category", "nutrition_grades", "stores"]
                aliment["category"] = category[0]
                data = []
                for header in headers:
                    try:
                        data.append("'" + aliment[header].replace("'", "\\'") + "'")
                    except KeyError:
                        data.append("NULL")
                    except AttributeError:
                        data.append(str(aliment[header]))
                self.insert("aliment", headers, data)
        clear()