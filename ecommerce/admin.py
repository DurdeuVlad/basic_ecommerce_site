from django.contrib import admin
from .models import Order, Product, ProductInOrder, ProductImage, Category, SubCategory, Settings, TrackingNumber, \
    SocialMediaLinks, CallToAction, TextLanguage, FrontPageProductShowcase, CarouselImage, EmailLog

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductInOrder)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Settings)
admin.site.register(TextLanguage)
admin.site.register(TrackingNumber)
admin.site.register(SocialMediaLinks)
admin.site.register(CallToAction)
admin.site.register(CarouselImage)
admin.site.register(FrontPageProductShowcase)
admin.site.register(EmailSender)

