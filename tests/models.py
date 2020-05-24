"""Provide Test Models for us to Use."""


from django.db import models



class Delivery(models.Model):

    address = models.CharField(max_length=32)

    @property
    def prop_address(self):
        return self.address


class DeliveryLine(models.Model):

    line_no = models.PositiveIntegerField()
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='delivery_lines')

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
'''



