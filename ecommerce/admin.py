from django.contrib import admin
from .models import Order, Product, ProductInOrder, ProductImages

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductInOrder)
admin.site.register(ProductImages)
