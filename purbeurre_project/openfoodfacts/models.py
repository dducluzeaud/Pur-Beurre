from django.db import models


class Categories(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    id_product = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    img = models.URLField()

    def __str__(self):
        return self.id_product, self.product_name, self.url, self.img


class Substitutes(models.Model):
    origin = models.ForeignKey(Products, related_name="origin", on_delete=models.CASCADE)
    replacement = models.ForeignKey(Products, related_name="replacement", on_delete=models.CASCADE)
