from rest_framework import serializers

from Online_Shop.orders.models import Order, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("quantity", 'product')

    def validate(self, attrs):
        product = attrs["product"]
        quantity = attrs["quantity"]
        if product.quantity < quantity:
            raise serializers.ValidationError(" Quantity is more than availability ")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["address"]
