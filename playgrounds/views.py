import json.decoder

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q, F
from django.http import HttpResponse
from store.models import Product, OrderItem

# Create your views here.
# request -> response
# This is a request handler

def calculate():
    x = 1
    y = 2
    return x + y

def say_hello(request):
    x = calculate()

    # query_list = Product.objects.all()  # this is lazy load
    # query_list.filter().filter().order_by()
    # Keyword = value
    # exists = Product.objects.filter(unit_price__gt=20)  # gt = greater than 20
    # querySet = Product.objects.filter(unit_price__range=(20, 30))  # range between 20 and 30
    # querySet = Product.objects.filter(collection__id__range=(20, 30, 40))  # id range between 20, 30 and 40
    # querySet = Product.objects.filter(title__icontains='coffee')  # all title contain 'coffee' (not case sensitive
    # because i)
    # querySet = Product.objects.filter(last_update__year=2021)  # last update on the year of 2021
    # querySet = Product.objects.filter(description__isnull=True)  # all product with missing description


    ###### complex query #####
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # inventory less than 10 or not unit_price less than 20
    # query_set = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20))

    # inventory less than 10 and unit_price less than 20
    # query_set = Product.objects.filter(Q(inventory__lt=10), Q(unit_price__lt=20))

    # get all product with inventory value equal to their collection__id value
    # query_set = Product.objects.filter(inventory=F('collection__id'))

    ##### sorting #####
    # query_set = Product.objects.order_by('title')  # sort the product by title in ASCENDING order
    # query_set = Product.objects.order_by('-title')  # sort the product by title in DESCENDING order

    # sort the product by unit_price first then by title in descending order
    # query_set = Product.objects.order_by('unit_price', '-title')

    # get the first product
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.latest('unit_price')

    ##### select #####
    # query_set = Product.objects.values('id', 'title')  # get only the 'title' and id 'field'

    # inner join collection with product and return the colum product.id, product.title, collection.title
    # query_set = Product.objects.values('id', 'title', 'collection__title')  # this will return a dictionary
    # query_set = Product.objects.values_list('id', 'title', 'collection__title')  # this will return a tuple

    # this will get all the product that has been ordered and sort them by title
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    # dont use defer or only or all
    # query_set = Product.objects.defer('id', 'title')
    # query_set = Product.objects.only('id', 'title')
    # query_set = Product.objects.all()

    # use selected_related (1)
    # query_set = Product.objects.select_related('collection').all()

    # prefetch_related (n)
    # query_set = Product.objects.prefetch_related('promotions').all()


    query_set = OrderItem.objects.prefetch_related('order__customer_id').select_related('product')

    return render(request, 'hello.html', {'name': 'Alex', 'products': list(query_set)})
