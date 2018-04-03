from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django.http import HttpResponseRedirect

@view_function
def process_request(request, pid):
    try:
        p = cmod.Product.objects.get(id = pid)
    except:
        return HttpResponseRedirect("/catalog/productlist")
    p.status = "inactive"
    p.save()
    return HttpResponseRedirect("/catalog/productlist")
