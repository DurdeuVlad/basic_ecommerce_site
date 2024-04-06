from django.db import models
from django.utils import timezone
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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
    image = models.ImageField(upload_to="ecommerce/images", default="")

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
    items_sold_DO_NOT_MODIFY = models.IntegerField(default=0)
    money_earned_DO_NOT_MODIFY = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # first call the original save method
        current_settings = Settings.objects.filter(active=True).first()
        if current_settings:
            top_n_products = Product.objects.order_by('-items_sold_DO_NOT_MODIFY')[
                             :current_settings.number_of_best_sellers]
        else:
            top_n_products = Product.objects.order_by('-items_sold_DO_NOT_MODIFY')[:5]

        Product.objects.update(is_best_seller=False)  # set all products to not best seller
        # top_n_products.update(is_best_seller=True)  # set top 5 products to best seller
        i = 0
        top_n_product_ids = Product.objects.order_by('-items_sold_DO_NOT_MODIFY').values_list('id', flat=True)[:top_n_products.count()]
        for product in top_n_products:
            if product.items_sold_DO_NOT_MODIFY <= 0:
                top_n_product_ids = Product.objects.order_by('-items_sold_DO_NOT_MODIFY').values_list('id', flat=True)[:i]
                break
            i += 1
            product.is_best_seller = True
        Product.objects.filter(id__in=top_n_product_ids).update(is_best_seller=True)



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

class SocialMediaIcons(models.TextChoices):
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"
    PINTEREST = "pinterest"
    SNAPCHAT = "snapchat"
    REDDIT = "reddit"
    TUMBLR = "tumblr"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    SKYPE = "skype"


class SocialMediaLinks(models.Model):
    id = models.AutoField(primary_key=True)
    settings = models.ForeignKey('Settings', on_delete=models.CASCADE)
    link = models.CharField(max_length=100, default="https://www.facebook.com/")
    icon = models.CharField(max_length=50, choices=SocialMediaIcons.choices, default=SocialMediaIcons.FACEBOOK)
    putInHeader = models.BooleanField(default=False)
    putInFooter = models.BooleanField(default=True)


class CallToAction(models.Model):
    id = models.AutoField(primary_key=True)
    settings = models.ForeignKey('Settings', on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default="Call to action")
    link = models.CharField(max_length=100, default="https://www.facebook.com/")
    fontAwesomeIconClassName = models.CharField(max_length=100, default="fas fa-shopping-cart")
    putInHeader = models.BooleanField(default=False)
    putInFooter = models.BooleanField(default=True)
    carouselImage = models.ForeignKey('CarouselImage', on_delete=models.CASCADE, null=True, blank=True)


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    test_mode = models.BooleanField(default=True)
    site_name = models.CharField(max_length=100, default="Ecommerce site")
    site_logo = models.ImageField(upload_to="ecommerce/images", default="")
    site_favicon = models.ImageField(upload_to="ecommerce/images", default="")
    site_description = models.CharField(max_length=100, default="Ecommerce site")
    email = models.CharField(max_length=100, default="user@gmail.com")
    currency = models.CharField(max_length=100, default="USD")
    currency_symbol = models.CharField(max_length=100, default="$")
    column_size_big_screen = models.IntegerField(default=5)
    column_size_short_screen = models.IntegerField(default=6)
    column_size_margin = models.IntegerField(default=4)
    items_per_page = models.IntegerField(default=12)
    product_last_chance_number = models.IntegerField(default=5)
    main_color = models.CharField(max_length=100, default="607D8B")
    secondary_color = models.CharField(max_length=100, default="3b71ca")
    navbar_color = models.CharField(max_length=100, default="FFFFFF")
    textLanguage = models.ForeignKey('TextLanguage', on_delete=models.CASCADE, default="1")
    number_of_best_sellers = models.IntegerField(default=5)
    
    # open_exchange_rates_api_key = models.CharField(max_length=100, default="GO ON THE WEBSITE AND GET YOUR OWN API KEY")
    # main_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default="1")


class TextLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="English")
    checkout_delete_button_text = models.CharField(max_length=100, default="Delete")
    product_last_chance_text = models.CharField(max_length=100, default="Last chance")
    product_best_seller_text = models.CharField(max_length=100, default="Best seller")
    buy_button_text = models.CharField(max_length=100, default="Buy now")
    product_new_text = models.CharField(max_length=100, default="New")
    product_featured_text = models.CharField(max_length=100, default="Featured")
    product_out_of_stock_text = models.CharField(max_length=100, default="Out of stock")


class FrontPageProductShowcase(models.Model):
    id = models.AutoField(primary_key=True)
    settings = models.ForeignKey('Settings', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Title")
    subtitle = models.CharField(max_length=100, default="Subtitle")
    description = models.CharField(max_length=100, default="Description")
    products = models.ManyToManyField(Product)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    new_products = models.BooleanField(default=False)
    best_sellers = models.BooleanField(default=False)
    featured_products = models.BooleanField(default=False)
    last_bought = models.BooleanField(default=False)
    last_seen = models.BooleanField(default=False)
    last_chance = models.BooleanField(default=False)
    promotion = models.BooleanField(default=False)


class CarouselImage(models.Model):
    id = models.AutoField(primary_key=True)
    settings = models.ForeignKey('Settings', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ecommerce/images", default="")
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default="Title")
    subtitle = models.CharField(max_length=100, default="Subtitle")
    description = models.CharField(max_length=100, default="Description")
    link = models.CharField(max_length=100, default="")


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    discount = models.PositiveIntegerField()