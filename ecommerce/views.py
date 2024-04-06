import stripe
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.db.models import F, Sum, Value, IntegerField, When, Case
from django.db.models.functions import Coalesce

from ecommerce import models
from ecommerce.models import Product, Order, ProductInOrder, Settings, SocialMediaLinks, CallToAction, CarouselImage


def start_page(request):
    # Get the current model settings
    setting = Settings.objects.filter(active=True).first()
    if setting is None:
        return catalog(request)

    # Get the social media links associated with the settings
    social_media_links = SocialMediaLinks.objects.filter(settings=setting)
    call_to_action_buttons = CallToAction.objects.filter(settings=setting)
    carousel_images = CarouselImage.objects.filter(settings=setting).order_by('order')
    return render(request, 'old_home.html', {'current_settings': setting, 'social_media_links': social_media_links,
                                         'call_to_action_buttons': call_to_action_buttons,
                                         'carousel_images': carousel_images})


# Create your views here.
def catalog(request, category_name=None, subcategory_name=None, products=None,
            name_search=None, page_number=1):
    # Create a Case expression for ordering
    ordering_case = Case(
        When(is_featured=True, then=Value(1)),
        When(is_best_seller=True, then=Value(2)),
        When(stock__gt=0, then=Value(3)),
        When(stock=0, then=Value(4)),
        default=Value(5),  # Default case, if any
        output_field=IntegerField()
    )

    if products is None:
        # Query each category and apply the ordering
        featured_products = Product.objects.filter(is_featured=True, stock__gt=0).annotate(order=ordering_case)
        best_seller_products = Product.objects.filter(is_best_seller=True, stock__gt=0).annotate(order=ordering_case)
        in_stock_products = Product.objects.filter(stock__gt=0).annotate(order=ordering_case)
        out_of_stock_products = Product.objects.filter(stock=0).annotate(order=ordering_case)

        # Combine the querysets
        all_products = featured_products | best_seller_products | in_stock_products | out_of_stock_products
        products = all_products.order_by('order', '-pub_date')


    else:
        # Order the combined queryset
        products = products.annotate(order=ordering_case)
        products = products.order_by('pub_date', '-pub_date')

    # Get rid of any product not from the requested category
    if category_name:
        products = products.filter(category__category_name=category_name)
        if subcategory_name:
            products = products.filter(category__subcategory__subcategory_name=subcategory_name)
    # Get the current category
    current_category = models.Category.objects.filter(category_name=category_name).first()
    all_categories = models.Category.objects.all()
    # get rid of any category that has no products
    all_categories = all_categories.annotate(
        num_products=Coalesce(Sum('product__stock'), Value(0), output_field=IntegerField())
    ).filter(num_products__gt=0)

    items_per_page = Settings.objects.filter(active=True).first().items_per_page
    # Paginate the queryset
    paginator = Paginator(products, items_per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    # Get how many pages there are
    num_pages = paginator.num_pages
    page_range = range(page_number - 1, page_number + 2)

    return render(request, 'catalog.html', {
        'all_products': page,
        'all_categories': all_categories,
        'current_category': current_category,
        'name_search': name_search,
        'page_number': page_number,
        'page_range': page_range,
        'num_pages': num_pages,
    })


def product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    return render(request, 'product.html', {'product': product})


def search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(product_name__icontains=query).order_by('product_name')
    return catalog(request, products=results, name_search=query)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if there is an existing order for the session
    order_id = request.session.get('order_id')

    if order_id is None:
        # If there is no existing order, create a new order
        order = Order.objects.create()
        request.session['order_id'] = order.order_id  # Use correct field name here
        order.order_session = request.session.session_key
    else:
        # If an order exists, fetch it
        order = Order.objects.get(order_id=order_id)  # Use correct field name here
    # search if the product is already in the order
    product_in_order = ProductInOrder.objects.filter(order=order, product=product).first()
    if product_in_order:
        # If the product is already in the order, increase the quantity
        product_in_order.quantity = F('quantity') + 1
        product_in_order.save()
    else:
        # Create a new ProductInOrder instance
        product_in_order = ProductInOrder.objects.create(
            order=order,
            product=product,
            quantity=1  # You can adjust the quantity as needed
        )
    # redirect to the same page
    order_id = request.session.get('order_id')
    order = Order.objects.filter(order_id=order_id).first()
    count = sum(product_in_order.quantity for product_in_order in order.productinorder_set.all())

    return JsonResponse({'cart_items_count': int(count)})


def checkout(request):
    if 'order_id' in request.session:
        order_id = request.session['order_id']
        order = Order.objects.get(pk=order_id)
        products_in_order = ProductInOrder.objects.filter(order=order)
        # calculate the total amount
        total_amount = 0
        for product_in_order in products_in_order:
            total_amount += product_in_order.product.price * product_in_order.quantity
        order.amount = total_amount
        # rest of your checkout logic
        return render(request, 'checkout.html', {'order': order, 'products_in_order': products_in_order})
    else:
        # If no 'order_id' is found, create an empty cart
        order = Order.objects.create(items_json='{}', amount=0)
        request.session['order_id'] = order.pk
        order.order_session = request.session.session_key
        products_in_order = ProductInOrder.objects.filter(order=order)
        # You can customize the message or behavior as needed
        return render(request, 'checkout.html', {'order': order, 'products_in_order': products_in_order})


def create_order(request):
    pass


def delete_from_cart(request, product_order_id):
    product_in_order = get_object_or_404(ProductInOrder, pk=product_order_id)
    # check if the product is in this session order
    if product_in_order.order.order_session == '':
        product_in_order.order.order_session = request.session.session_key
    if request.session.session_key == product_in_order.order.order_session:
        product_in_order.delete()
    return redirect('checkout')


def increment_quantity(request, product_order_id, quantity=1):
    product_in_order = get_object_or_404(ProductInOrder, pk=product_order_id)
    # check if the product is in this session order
    if product_in_order.order.order_session == '':
        product_in_order.order.order_session = request.session.session_key
    if request.session.session_key == product_in_order.order.order_session:
        product_in_order.quantity += quantity
        product_in_order.save()
    return redirect('checkout')


def decrement_quantity(request, product_order_id, quantity=-1):
    return increment_quantity(request, product_order_id, quantity)


def cart_items_count(request):
    order_id = request.session.get('order_id')

    # Check if order_id exists in session
    if order_id is not None:
        order = Order.objects.filter(order_id=order_id).first()

        # Check if order exists
        if order is not None:
            count = 0
            for product_in_order in order.productinorder_set.all():
                count += product_in_order.quantity
            return {'cart_items_count': count}

    # Return default count if order is not found
    return {'cart_items_count': 0}


def current_settings(request):
    # Get the current model settings
    setting = Settings.objects.filter(active=True).first()
    # Get the social media links associated with the settings
    social_media_links = SocialMediaLinks.objects.filter(settings=setting)
    call_to_action_buttons = CallToAction.objects.filter(settings=setting)
    carousel_images = CarouselImage.objects.filter(settings=setting).order_by('order')
    return {'current_settings': setting, 'social_media_links': social_media_links,
            'call_to_action_buttons': call_to_action_buttons, 'carousel_images': carousel_images}


def cart_count(request):
    order_id = request.session.get('order_id')
    order = Order.objects.filter(order_id=order_id).first()
    count = sum(product_in_order.quantity for product_in_order in order.productinorder_set.all())

    return JsonResponse({'cart_items_count': int(count)})

def send_email(request):
    if request.method == 'POST':
        # Retrieve data from request
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        to_email = request.POST.get('to_email')

        # Get SMTP settings from Settings model or wherever they are stored
        smtp_server = Settings.objects.get().smtp_server
        smtp_port = Settings.objects.get().smtp_port
        smtp_username = Settings.objects.get().smtp_username
        smtp_password = Settings.objects.get().smtp_password

        # Create an instance of EmailSender with SMTP settings
        email_sender = EmailSender(smtp_server, smtp_port, smtp_username, smtp_password)

        # Send email
        email_sender.send_email(subject, body, to_email)

        # Optionally, add some logic to handle success or failure
        # For example, return a success message or redirect to a different page

        # Return an HTTP response
        return HttpResponse("Email sent successfully!")
    else:
        # Handle GET requests if needed
        pass
