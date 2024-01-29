from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone

from ecommerce.models import Product


# Create your views here.
def home(request):
    week_ago = timezone.now() - timedelta(days=7)
    in_stock_products = Product.objects.filter(stock__gt=0, pub_date__lt=week_ago).order_by('-pub_date')
    new_stock_products = Product.objects.filter(stock__gt=0, pub_date__gte=week_ago).order_by('-pub_date')
    out_of_stock_products = Product.objects.filter(stock=0).order_by('-pub_date')
    return render(request, 'index.html',
                    {'new_stock_products': new_stock_products, 'in_stock_products': in_stock_products, 'out_of_stock_products': out_of_stock_products})

