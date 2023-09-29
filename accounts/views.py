import json

from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import authenticate
from django.core.cache import caches

from .models import Address
from .serializers import UserRegisterSerializer, UserLoginSerializer, ProfileSerializer, ChangePasswordSerializer, \
    UpdateUserSerializer, UserAddressSerializer
from .authentication import AccessTokenAuthentication, RefreshTokenAuthentication
from .utils import generate_refresh_token, generate_access_token, jti_maker, cache_key_setter, cache_value_setter, \
    cache_key_or_value_parser

from orders.models import CartItem

from Permissions import UserIsOwner


# Create your views here.


class UserRegister(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_identifier = serializer.validated_data.get('user_identifier')
        password = serializer.validated_data.get('password')
        user = authenticate(request, user_identifier=user_identifier, password=password)
        if user is None:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        jti = jti_maker()
        access_token = generate_access_token(user.id, jti)
        refresh_token = generate_refresh_token(user.id, jti)
        key = cache_key_setter(user.id, jti)
        value = cache_value_setter(request)
        caches['auth'].set(key, value)

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }

        cart = request.COOKIES.get('cart')
        if cart:
            cart = json.loads(cart)
            # cart_obj_list = []
            for product_id, quantity in cart.items():
                cart, created = CartItem.objects.get_or_create(user=user, product_id=product_id)

                if created:
                    cart.quantity = quantity
                else:
                    cart.quantity += quantity
                cart.save()

            #     cart_obj_list.append(cart)
            #
            # CartItem.objects.bulk_create(cart_obj_list)

        return Response(data, status=status.HTTP_201_CREATED)


class RefreshToken(APIView):
    authentication_classes = (RefreshTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        payload = request.auth

        jti = payload["jti"]
        caches['auth'].delete(f'user_{user.id} || {jti}')

        jti = jti_maker()
        access_token = generate_access_token(user.id, jti)
        refresh_token = generate_refresh_token(user.id, jti)

        key = cache_key_setter(user.id, jti)
        value = cache_value_setter(request)
        caches['auth'].set(key, value)

        data = {
            "access": access_token,
            "refresh": refresh_token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    authentication_classes = (RefreshTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            payload = request.auth
            user = request.user
            jti = payload["jti"]
            caches['auth'].delete(f'user_{user.id} || {jti}')

            return Response({"message": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckAllActiveLogin(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        payload = request.auth
        user = request.user
        jti = payload["jti"]

        active_login_data = []
        for value in caches['auth'].get_many(caches['auth'].keys(f'user_{user.id} || *')).values():
            user_agent = cache_key_or_value_parser(value)[0]
            OS_accounts = cache_key_or_value_parser(value)[1]

            active_login_data.append({
                "jti": jti,
                "user_agent": user_agent,
                "OS_accounts": OS_accounts,
            })

        return Response(active_login_data, status=status.HTTP_200_OK)


class LogoutAll(APIView):
    authentication_classes = (RefreshTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        caches['auth'].delete_many(caches['auth'].keys(f'user_{user.id} || *'))

        return Response({"message": "All accounts logged out"}, status=status.HTTP_200_OK)


class SelectedLogout(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        jti = request.data.get("jti")
        caches['auth'].delete(f'user_{user.id} || {jti}')

        return Response({"message": True}, status=status.HTTP_200_OK)


class ShowProfile(APIView):
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request):
        user = request.user
        ser_data = self.serializer_class(user)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    http_method_names = ["patch"]
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Password has been successfully updated"})

    def get_object(self):
        return self.request.user


class UpdateProfileView(UpdateAPIView):
    http_method_names = ["patch"]
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


class CreateAddress(CreateAPIView):
    http_method_names = ["post"]
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RemoveAddress(DestroyAPIView):
    http_method_names = ["delete"]
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated, UserIsOwner)
    queryset = Address.objects.all()


class AddressList(ListAPIView):
    http_method_names = ["get"]
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class UpdateAddress(UpdateAPIView):
    http_method_names = ["patch"]
    authentication_classes = (AccessTokenAuthentication,)
    permission_classes = (IsAuthenticated, UserIsOwner)
    serializer_class = UserAddressSerializer
    queryset = Address.objects.all()


class GetAddress(RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer