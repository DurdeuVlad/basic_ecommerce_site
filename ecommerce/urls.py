from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.catalog, name="home"),  # Default home URL
    path("home/", views.catalog, name="home"),  # Default home URL
    path("catalog/", views.catalog, name="catalog"),  # Default home URL
    path('categories/', views.catalog, name="home"),  # Home URL for categories
    path('categories/<str:category_name>/', views.catalog, name='home'),
    path('product/<int:product_id>/', views.product, name='product'),  # URL for a specific product
    path('search/', views.search, name='search'),  # Add this line
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('delete_from_cart/<int:product_order_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('ajax/cart_count/', views.cart_count, name='cart_count'),
    path('page/<int:page_number>/', views.catalog, name='page'),
    path('increment_quantity/<int:product_order_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:product_order_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('contact/', views.contact_us, name='contact_us'),
]
