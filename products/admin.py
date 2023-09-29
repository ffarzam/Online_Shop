from django.contrib import admin
from .models import Products, Brand, Feature,ProductDetails, Image

# Register your models here.

admin.site.register(Products)
admin.site.register(Brand)
admin.site.register(Feature)
admin.site.register(ProductDetails)
admin.site.register(Image)
