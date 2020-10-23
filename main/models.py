from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, default=None)
    url = models.CharField(max_length=128, default=None)


class Aliment(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=128, default=None, unique=True, null=True, blank=True)
    nutrition_grades = models.CharField(max_length=1, default=None, null=True, blank=True)
    stores = models.CharField(max_length=128, default=None, null=True, blank=True)
    image_front_thumb_url = models.CharField(max_length=255, default=None, null=True, blank=True)
    url = models.CharField(max_length=255, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Substitute(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=128, default=None, unique=True, null=True, blank=True)
    nutrition_grades = models.CharField(max_length=1, default=None, null=True, blank=True)
    stores = models.CharField(max_length=128, default=None, null=True, blank=True)
    image_front_thumb_url = models.CharField(max_length=255, default=None, null=True, blank=True)
    url = models.CharField(max_length=255, default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
