from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod

@view_function
def process_request(request):
    context = {

        'product_list': cmod.Product.objects.filter(status = "active"),

    }
    return request.dmp.render('productlist.html', context)
