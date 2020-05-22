"""Provide Test Models for us to Use."""


from django.db import models


# Create your models here.
class Product(models.Model):

    name = models.CharField(max_length=32)
    price = models.DecimalField()

'''
class DeliveryLine(models.Model):


    fields and properties


class Delivery(models.Model):

    fields and properties
'''



