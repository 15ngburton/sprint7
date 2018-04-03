from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from catalog import models as cmod
from django.contrib import auth
import math

@view_function
def process_request(request, catID:int=0, page_num:int=1):
    category_list = cmod.Category.objects.all()
    if catID == 0:
        product_list = cmod.Product.objects.filter(status = "A")
        category = "All Products"
    else:
        product_list = cmod.Product.objects.filter(category_id = catID, status = "A")
        category = cmod.Category.objects.get(id = catID).name

    num_of_pages = math.ceil(product_list.count() / 6)

    context = {
        'category': category,
        "category_list": category_list,
        'page_num': page_num,
        'num_of_pages': num_of_pages,
        'catID': catID,
    }

    return request.dmp.render('index.html', context)
