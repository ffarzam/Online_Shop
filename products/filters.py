import django_filters
from django_filters.rest_framework import FilterSet
from .models import Products


class ProductsFilter(FilterSet):
    # uncategorized = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Products
        fields = {
            'brand__title': ['exact'],
            'price': ['gte', 'lte'],
            'product_year': ['gte', 'lte'],
            'description': ['in', 'exact'],
        }
