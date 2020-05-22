"""Provide Test Models for us to Use."""


from django.db import models


class DeliveryLine(models.Model):

    line_no = models.PositiveIntegerField()

    @property
    def prop_line_no(self):
        return self.line_no


class Product(models.Model):

    name = models.CharField(max_length=32)
    price = models.DecimalField()
    del_line = models.ForeignKey(DeliveryLine, on_delete=models.CASCADE, related_name='products')

    @property
    def prop_name(self):
        return self.name

    @property
    def prop_line_no(self):
        return self.del_line.line_no

'''
class Delivery(models.Model):

    fields and properties
'''



