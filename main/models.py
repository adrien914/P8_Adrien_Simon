from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)


# Create your models here.
class Aliment(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=128, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutrition_grades = models.CharField(max_length=1, default=None)
    stores = models.CharField(max_length=128, default=None)


class Substitute(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=128, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutrition_grades = models.CharField(max_length=1, default=None)
    stores = models.CharField(max_length=128, default=None)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
