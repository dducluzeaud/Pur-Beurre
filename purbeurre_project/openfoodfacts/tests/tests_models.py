from django.test import TestCase
from openfoodfacts.models import Categories, Products


class CategoriesTestCase(TestCase):
    def setUp(self):
        Categories.objects.create(category_name="confitures")

    def test_category_name(self):
        marmelade = Categories.objects.get(category_name="confitures")
        self.assertEqual("confitures", marmelade.category_name)


class ProductsTestCase(TestCase):
    def setUp(self):
        Products.objects.create(id_product=1, product_name="nutella", url="http://", img="http://")

    def test_id_product(self):
        nutella = Products.objects.get(id_product=1)
        self.assertEqual(1, nutella.id_product)

    def test_product_name(self):
        nutella = Products.objects.get(product_name="nutella")
        self.assertEqual("nutella", nutella.product_name)

    def test_url(self):
        nutella = Products.objects.get(url="http://")
        self.assertEqual("http://", nutella.url)

    def test_img(self):
        nutella = Products.objects.get(url="http://")
        self.assertEqual("http://", nutella.img)
