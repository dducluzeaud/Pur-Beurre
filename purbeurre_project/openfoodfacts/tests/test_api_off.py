import urllib3
import json
from io import BytesIO

from openfoodfacts.models import Categories, Products
from openfoodfacts.management.commands.api_off import Command
from django.test import TestCase



class CommandTestCase(TestCase):
    def setUp(self):
        self.com = Command()
        self.category = "Fromages"
        prod_data = {
            "product_name": "Comté",
            "product_id": 123,
            "product_url": "http://",
            "product_img": "http://",
            "nutriscore": "c"
            }
        self.content = [prod_data]

    def test_handle(self):
        pass


    def test_request_api(self):

        json_results = "openfoodfacts/tests/mock_folder/off.json"
        mock = json.loads(json_results)

        monkeypatch.setattr(urllib3.request, 'urlopen', mockreturn)
        self.assertEqual(Command.request_api, json_results)

    def test_insert(self):
        self.com._insert(self.content, self.category)

        prod = Products.objects.get()
        cat = Categories.objects.get()

        self.assertEqual(cat.id, 1)
        self.assertEqual(cat.category_name, "Fromages")
        self.assertEqual(prod.product_name, "Comté")
        self.assertEqual(prod.id_product, 123)
        self.assertEqual(prod.url, "http://")
        self.assertEqual(prod.img, "http://")
        self.assertEqual(prod.nutriscore, "c")
        self.assertEqual(str(prod.category), cat.category_name)
