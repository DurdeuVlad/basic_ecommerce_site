from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class OrderStatus(models.TextChoices):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_session = models.CharField(max_length=500, default="", help_text="Enter order session")
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING,
                              help_text="Select order status")
    payment_method = models.CharField(max_length=500, default="", help_text="Select payment method")
    items_json = models.CharField(max_length=5000, help_text="Paste item JSON")
    amount = models.IntegerField(default=0, help_text="Enter amount")
    name = models.CharField(max_length=50, help_text="Enter your name")
    email = models.CharField(max_length=50, help_text="Enter email address")
    address = models.CharField(max_length=50, help_text="Enter first address")
    address2 = models.CharField(max_length=50, help_text="Enter second address")
    city = models.CharField(max_length=50, help_text="Enter city")
    state = models.CharField(max_length=50, help_text="Enter state")
    zip_code = models.CharField(max_length=50, help_text="Enter zip code")
    phone = models.CharField(max_length=50, default="", help_text="Enter phone number")

    def __str__(self):
        return self.name


class TrackingNumber(models.Model):
    id = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="Enter order ID")
    tracking_number = models.CharField(max_length=50, default="", help_text="Enter tracking number")

    def __str__(self):
        return self.tracking_number


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, default="Category name", help_text="Enter category name")
    image = models.ImageField(upload_to="ecommerce/images", default="", help_text="Select image")

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=50, default="Subcategory name", help_text="Enter subcategory name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Select category")

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, default="Name", help_text="Enter product name")
    price = models.IntegerField(default=0, help_text="Enter product price")
    stock = models.IntegerField(default=0, help_text="Enter product stock")
    desc = models.CharField(max_length=100, default="Short description to appear on the home page and next to the "
                                                    "product.", help_text="Write a short description")
    additional_info = models.CharField(max_length=600, default="Longer description to appear on the product page. If "
                                                               "you dont want any info here"
                                                               " just leave it blank.",
                                       help_text="Enter additional information")
    pub_date = models.DateTimeField(default=timezone.now, help_text="Enter publish date")
    thumbnail = models.ImageField(upload_to="ecommerce/images", default="", help_text="Select thumbnail")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="0", help_text="Select category")
    is_best_seller = models.BooleanField(default=False, help_text="Tick this if the product is a best seller")
    is_featured = models.BooleanField(default=False, help_text="Tick this if the product is featured")
    is_new = models.BooleanField(default=False, help_text="Tick this if the product is new")
    items_sold_DO_NOT_MODIFY = models.IntegerField(default=0, help_text="Items sold")
    money_earned_DO_NOT_MODIFY = models.IntegerField(default=0, help_text="Money earned")

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
        top_n_product_ids = Product.objects.order_by('-items_sold_DO_NOT_MODIFY').values_list('id', flat=True)[
                            :top_n_products.count()]
        for product in top_n_products:
            if product.items_sold_DO_NOT_MODIFY <= 0:
                top_n_product_ids = Product.objects.order_by('-items_sold_DO_NOT_MODIFY').values_list('id', flat=True)[
                                    :i]
                break
            i += 1
            product.is_best_seller = True
        Product.objects.filter(id__in=top_n_product_ids).update(is_best_seller=True)

    def __str__(self):
        return self.product_name


class ProductInOrder(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Select a product")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, help_text="Select order")
    quantity = models.IntegerField(default=1, help_text="Enter quantity")

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Select product")
    image = models.ImageField(upload_to="ecommerce/images", default="", help_text="Select product image")

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
    link = models.CharField(max_length=100, default="https://www.facebook.com/",
                            help_text="Enter social media link here")
    icon = models.CharField(max_length=50, choices=SocialMediaIcons.choices, default=SocialMediaIcons.FACEBOOK,
                            help_text="Select an icon")
    putInHeader = models.BooleanField(default=False, help_text="Put link in header")
    putInFooter = models.BooleanField(default=True, help_text="Put link in footer")


class CallToAction(models.Model):
    id = models.AutoField(primary_key=True)
    settings = models.ForeignKey('Settings', on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default="Call to action", help_text="Add a call to action here")
    link = models.CharField(max_length=100, default="https://www.facebook.com/",
                            help_text="Enter your social media link here")
    fontAwesomeIconClassName = models.CharField(max_length=100, default="fas fa-shopping-cart")
    putInHeader = models.BooleanField(default=False, help_text="Put in header")
    putInFooter = models.BooleanField(default=True, help_text="Put in footer")
    carouselImage = models.ForeignKey('CarouselImage', on_delete=models.CASCADE, null=True, blank=True)


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True, help_text="Tick this if active")
    test_mode = models.BooleanField(default=True, help_text="Tick this if in test mode")
    site_name = models.CharField(max_length=100, default="Ecommerce site", help_text="Enter site name")
    site_logo = models.ImageField(upload_to="ecommerce/images", default="", help_text="Select logo")
    site_favicon = models.ImageField(upload_to="ecommerce/images", default="", help_text="Select icon")
    site_description = models.CharField(max_length=100, default="Ecommerce site", help_text="Write a short description")
    email = models.CharField(max_length=100, default="user@gmail.com", help_text="Enter company email address")
    currency = models.CharField(max_length=100, default="USD", help_text="Select currency")
    currency_symbol = models.CharField(max_length=100, default="$", help_text="Select currency symbol")
    column_size_big_screen = models.IntegerField(default=5, help_text="Enter column big screen size")
    column_size_short_screen = models.IntegerField(default=6, help_text="Enter column short screen size")
    column_size_margin = models.IntegerField(default=4, help_text="Enter column margin")
    items_per_page = models.IntegerField(default=12, help_text="How many items will be displayed on the page")
    product_last_chance_number = models.IntegerField(default=5,
                                                     help_text="How many last chance items will be displayed")
    main_color = models.CharField(max_length=100, default="607D8B", help_text="Select main color")
    secondary_color = models.CharField(max_length=100, default="3b71ca", help_text="Select secondary color")
    navbar_color = models.CharField(max_length=100, default="FFFFFF", help_text="Select navbar color")
    textLanguage = models.ForeignKey('TextLanguage', on_delete=models.CASCADE, default="1", help_text="Select language")
    number_of_best_sellers = models.IntegerField(default=5, help_text="Enter number of best sellers your company has")
    # open_exchange_rates_api_key = models.CharField(max_length=100, default="GO ON THE WEBSITE AND GET YOUR OWN API KEY")
    # main_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default="1")

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_email(subject, body, to_email):
        # Set up SMTP server
        smtp_server = 'your_smtp_server'
        smtp_port = 587  # Change to your SMTP server's port
        smtp_username = 'your_smtp_username'
        smtp_password = 'your_smtp_password'

        # Create message
        msg = MIMEMultipart()
        msg['From'] = 'your_email@example.com'
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach body
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send email
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        # Close connection
        server.quit()




class TextLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="English", help_text="Enter language")
    checkout_delete_button_text = models.CharField(max_length=100, default="Delete",
                                                   help_text="Enter delete button text")
    product_last_chance_text = models.CharField(max_length=100, default="Last chance",
                                                help_text="Enter last chance text")
    product_best_seller_text = models.CharField(max_length=100, default="Best seller",
                                                help_text="Enter best seller text")
    buy_button_text = models.CharField(max_length=100, default="Buy now", help_text="Enter buy now text")
    product_new_text = models.CharField(max_length=100, default="New", help_text="Enter new product text")
    product_featured_text = models.CharField(max_length=100, default="Featured", help_text="Enter featured text")
    product_out_of_stock_text = models.CharField(max_length=100, default="Out of stock",
                                                 help_text="Enter out of stock text")


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
