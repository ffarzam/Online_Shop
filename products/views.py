from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_redis import get_redis_connection
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .filters import ProductsFilter
from .models import Products, Brand
from .serializer import ProductSerializer, BrandSerializer
from .utils import ProductsPagination


# Create your views here.


class ProductList(ListAPIView):
    queryset = Products.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'product_year', 'price']
    filterset_class = ProductsFilter


class GetProduct(RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class SearchView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        search_query = self.request.query_params["search"]

        products_search_results = Products.objects.select_related("brand").filter(
            Q(name__icontains=search_query) | Q(
                description__icontains=search_query) | Q(
                brand__title__icontains=search_query)).distinct()

        return products_search_results


class BrandList(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
