from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, default=None)
    url = models.CharField(max_length=128, default=None)


class Aliment(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=128, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutrition_grades = models.CharField(max_length=1, default=None, null=True, blank=True)
    stores = models.CharField(max_length=128, default=None, null=True, blank=True)

    def __str__(self):
        return self.product_name

class Substitute(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=128, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutrition_grades = models.CharField(max_length=1, default=None, null=True, blank=True)
    stores = models.CharField(max_length=128, default=None, null=True, blank=True)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
