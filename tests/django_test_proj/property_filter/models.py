from django.db import models

# Create your models here.
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
    price = models.DecimalField(decimal_places=2, max_digits=10)
    del_line = models.ForeignKey(DeliveryLine, on_delete=models.CASCADE, related_name='products')

    @property
    def prop_name(self):
        return self.name

    @property
    def prop_line_no(self):
        return self.del_line.line_no


class NumberClass(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    @property
    def prop_number_2(self):
        return self.number

    def __str__(self):
        return F'{self.number}'


class BooleanClass(models.Model):
    is_true = models.BooleanField(null=True)

    @property
    def prop_is_true(self):
        return self.is_true

    def __str__(self):
        return F'{self.is_true} ({self.id})'


class TextClass(models.Model):
    name = models.CharField(max_length=32)

    @property
    def prop_name(self):
        return self.name

    def __str__(self):
        return F'{self.name} ({self.id})'


class DateClass(models.Model):
    date = models.DateField()

    @property
    def prop_date(self):
        return self.date

    def __str__(self):
        return F'{self.date} ({self.id})'


class TimeClass(models.Model):
    time = models.TimeField()

    @property
    def prop_time(self):
        return self.time

    def __str__(self):
        return F'{self.time} ({self.id})'


class DurationClass(models.Model):
    duration = models.DurationField()

    @property
    def prop_duration(self):
        return self.duration

    def __str__(self):
        return F'{self.duration} ({self.id})'
