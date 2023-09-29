from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import AccessTokenAuthentication

from Online_Shop.orders.models import OrderDetail, Order
from Online_Shop.orders.serializer import OrderSerializer
from .models import CartItem
from .serializer import CartItemSerializer


# Create your views here.


class CreateCartItem(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        ser_data.is_valid(raise_exception=True)
        quantity = ser_data.validated_data["quantity"]
        product = ser_data.validated_data["product"]
        cart, created = CartItem.objects.get_or_create(user=request.user, product=product)
        cart.quantity = quantity
        return Response({"message": "Items added to cart"}, status=status.HTTP_200_OK)


class ShowCartItem(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemSerializer

    def get(self, request):
        user = request.user
        cart_items = CartItem.get_cart_item(user=user)
        serializer = self.serializer_class(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCartItem(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemSerializer

    def get(self, request):
        user = request.user
        ser_data = self.serializer_class(data=request.POST)
        ser_data.is_valid(raise_exception=True)
        product = ser_data.validated_data["product"]
        CartItem.objects.filter(user=user, product=product).delete()
        return Response({"message": "Delete Complete"}, status=status.HTTP_200_OK)


class UpdateCartItem(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemSerializer

    def get(self, request):
        user = request.user
        ser_data = self.serializer_class(data=request.POST)
        ser_data.is_valid(raise_exception=True)
        quantity = ser_data.validated_data["quantity"]
        product = ser_data.validated_data["product"]
        cart_item = CartItem.objects.get(user=user, product=product)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"message": "Update Complete"}, status=status.HTTP_200_OK)


class CreateOrder(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def post(self, request):
        user = request.user
        serialized = self.serializer_class(request.data)
        serialized.is_valid(raise_exception=True)
        address = serialized.validated_data["address"]
        order_obj = Order.objects.create(user=user, address=address)

        cart_items = CartItem.get_cart_item(user=user)
        order_details_obj_list = []
        unavailable = []
        with transaction.atomic:
            for cart_item in cart_items:
                if cart_item.product.quantity > cart_item.quantity:
                    order_details_obj = OrderDetail(order=order_obj,
                                                    product=cart_item.product,
                                                    quantity=cart_item.quantity,
                                                    price=cart_item.product.price)

                    order_details_obj_list.append(order_details_obj)
                    cart_item.delete()
                    cart_item.product.quantity -= cart_item.quantity
                else:
                    unavailable.append(cart_item.product.id)

            if len(unavailable) != 0:
                raise ValueError

            OrderDetail.objects.bulk_create(order_details_obj_list)

        if len(unavailable) == 0:
            CartItem.objects.filter(product_id__in=unavailable).delete()
            qs = CartItem.objects.filter(user=user)
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Order has been created!", status=status.HTTP_201_CREATED)
