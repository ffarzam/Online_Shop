from django.db import models


# Create your models here.

class Brand(models.Model):
    title = models.CharField(max_length=50)


class Feature(models.Model):
    color = models.CharField(max_length=25)
    ram = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()


class Products(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    product_year = models.PositiveIntegerField()
    feature = models.OneToOneField(Feature, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField()


class Image(models.Model):
    products = models.ForeignKey(Products, on_delete=models.PROTECT)
    is_main = models.BooleanField()
    image = models.FileField(upload_to="products_image")
