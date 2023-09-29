from django.urls import path
from . import views


urlpatterns = [
    path('create_cart_item/', views.CreateCartItem.as_view(), name='create_cart_item'),
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),

]


