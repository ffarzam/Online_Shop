from django.db import models


# Create your models here.

class Brand(models.Model):
    title = models.CharField(max_length=50)


class Feature(models.Model):
    feature_key = models.CharField(max_length=50)
    feature_value = models.CharField(max_length=50)

    class Meta:
        unique_together = ('feature_key', 'feature_value',)


class Products(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    product_year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField()


class Image(models.Model):
    products = models.ForeignKey(Products, on_delete=models.PROTECT)
    is_main = models.BooleanField()
    image = models.FileField(upload_to="products_image")


class ProductDetails(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
