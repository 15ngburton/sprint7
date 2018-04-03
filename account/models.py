from django.db import models

from cuser.models import AbstractCUser


class User(AbstractCUser):
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)

    def get_purchases(self):
        return [ 'Roku ultimate 2000', 'USB Cable', 'Candy Bar']
