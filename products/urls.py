from django.urls import path
from . import views


urlpatterns = [
    path('products_list/', views.ProductList.as_view(), name='products_list'),
    path('product/<int:pk>', views.GetProduct.as_view(), name='product'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('brand_list/', views.BrandList.as_view(), name='brand_list'),

]


