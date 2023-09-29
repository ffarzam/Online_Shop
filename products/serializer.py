from rest_framework import serializers

from .models import Products, Brand


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"



