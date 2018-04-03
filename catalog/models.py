from django.db import models
import datetime
from polymorphic.models import PolymorphicModel


class Category(models.Model):
    name = models.TextField(blank=True, null=False)
    description = models.TextField(blank=True, null=False)
    #The following update automatically
    create_date = models.DateTimeField(blank=True, null=True, auto_now_add = True)
    last_modified = models.DateTimeField(blank=True, null=True, auto_now = True)

    def __str__(self):
        return u'{0}'.format(self.name)

class Product(PolymorphicModel):
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE, null = True)
    name = models.TextField(blank=True, null=False)
    description = models.TextField(blank=True, null=False)
    price = models.DecimalField(blank=True, null=False, max_digits=20, decimal_places=2)
    status = models.TextField(blank = True, null = False)
    #The following update automatically
    create_date = models.DateTimeField(blank=True, null=True, auto_now_add = True)
    last_modified = models.DateTimeField(blank=True, null=True, auto_now = True)

    def image_url(self):
        '''Always returns an image'''
        if (len(list(self.images.all())) != 0):
            return "catalog/media/products/" + list(self.images.all())[0].filename
        else:
            return "catalog/media/products/notfound.jpg"

    def image_urls(self):
        urlList = []
        if (len(list(self.images.all())) != 0):
            for img in list(self.images.all()):
                urlList.append("catalog/media/products/" + img.filename)
            return urlList
        else:
            urlList.append("catalog/media/products/notfound.jpg")
            return urlList


class IndividualProduct(Product):
    pid = models.TextField(blank = True, null = False)

class BulkProduct(Product):
    quantity = models.IntegerField(blank = True, null = False)
    reorder_trigger = models.IntegerField(blank = True, null = False)
    reorder_quantity = models.IntegerField(blank = True, null = False)

class RentalProduct(Product):
    pid = models.TextField(blank = True, null = False)
    max_rental_days = models.IntegerField(blank = True, null = False)
    retire_date = models.DateTimeField(blank = True, null = True)

class ProductImage(models.Model):
	filename = models.TextField(blank = True, null = True)
	product = models.ForeignKey("Product", on_delete = models.CASCADE, related_name="images")
