from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Default home URL
    path("home/", views.home, name="home"),  # Default home URL
    path('categories/', views.home, name="home"),  # Home URL for categories
    path('categories/<str:category_name>/', views.home, name='home'),
    path('product/<int:product_id>/', views.product, name='product'),  # URL for a specific product
    path('search/', views.search, name='search'),  # Add this line
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('delete_from_cart/<int:product_order_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('ajax/cart_count/', views.cart_count, name='cart_count'),
]
