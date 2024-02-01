from django.db import models
from django.utils import timezone

class OrderStatus(models.TextChoices):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_session = models.CharField(max_length=500, default="")
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_method = models.CharField(max_length=500, default="")
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class TrackingNumber(models.Model):
    id = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.tracking_number


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, default="Category name")

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=50, default="Subcategory name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, default="Name")
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    desc = models.CharField(max_length=100, default="Short description to appear on the home page and next to the "
                                                    "product.")
    additional_info = models.CharField(max_length=600, default="Longer description to appear on the product page. If "
                                                               "you dont want any info here"
                                                               " just leave it blank.")
    pub_date = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to="ecommerce/images", default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="0")
    is_best_seller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    pieces_sold_DO_NOT_MODIFY = models.IntegerField(default=0)
    money_earned_DO_NOT_MODIFY = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class ProductInOrder(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ecommerce/images", default="")

    def __str__(self):
        return self.product.product_name + " image"


# class Currency(models.Model):
#    id = models.AutoField(primary_key=True)
#    currency_name = models.CharField(max_length=50, default="USD")
#    currency_symbol = models.CharField(max_length=50, default="$")
#    exchange_rate_USD = models.FloatField(default=1.0)


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    test_mode = models.BooleanField(default=True)
    site_name = models.CharField(max_length=100, default="Ecommerce site")
    site_logo = models.ImageField(upload_to="ecommerce/images", default="")
    site_favicon = models.ImageField(upload_to="ecommerce/images", default="")
    site_description = models.CharField(max_length=100, default="Ecommerce site")
    facebook_link = models.CharField(max_length=100, default="https://www.facebook.com/")
    twitter_link = models.CharField(max_length=100, default="https://twitter.com/")
    instagram_link = models.CharField(max_length=100, default="https://www.instagram.com/")
    youtube_link = models.CharField(max_length=100, default="https://www.youtube.com/")
    email = models.CharField(max_length=100, default="user@gmail.com")
    phone = models.CharField(max_length=100, default="1234567890")
    address = models.CharField(max_length=100, default="1234 Main St")
    address2 = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="Anytown")
    state = models.CharField(max_length=100, default="NY")
    zip_code = models.CharField(max_length=100, default="12345")
    currency = models.CharField(max_length=100, default="USD")
    currency_symbol = models.CharField(max_length=100, default="$")
    STRIPE_LIVE_PUBLIC_KEY = models.CharField(max_length=100, default="GO ON THE WEBSITE AND GET YOUR OWN API KEY")
    STRIPE_LIVE_SECRET_KEY = models.CharField(max_length=100, default="GO ON THE WEBSITE AND GET YOUR OWN API KEY")
    STRIPE_TEST_PUBLIC_KEY = models.CharField(max_length=100, default="GO ON THE WEBSITE AND GET YOUR OWN API KEY")
    STRIPE_TEST_SECRET_KEY = models.CharField(max_length=100, default="GO ON THE WEBSITE AND GET YOUR OWN API KEY")
    # open_exchange_rates_api_key = models.CharField(max_length=100, default="GO ON THE WEBSITE AND GET YOUR OWN API KEY")
    # main_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default="1")
