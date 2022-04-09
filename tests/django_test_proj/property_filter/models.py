from django.db import models

import django_filters.fields

try:
    from django.contrib.postgres.fields import DecimalRangeField, IntegerRangeField
except ImportError:
    pass

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


class DoubleIntModel(models.Model):
    age = models.IntegerField()
    number = models.IntegerField()

    @property
    def prop_age(self):
        return self.age

    @property
    def prop_number(self):
        return self.number


class AllValuesFilterModel(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number} ({self.id})'


class AllValuesMultipleFilterModel(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number} ({self.id})'


class BaseCSVFilterModel(models.Model):
    number = models.IntegerField(null=True)
    text = models.CharField(max_length=32)

    @property
    def prop_number(self):
        return self.number

    @property
    def prop_text(self):
        return self.text

    def __str__(self):
        return F'{self.number} - "{self.text}" ({self.id})'


class BaseInFilterModel(models.Model):
    number = models.DecimalField(decimal_places=2, max_digits=10)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number} ({self.id})'


class BaseRangeFilterModel(models.Model):
    date = models.DateField()

    @property
    def prop_date(self):
        return self.date

    def __str__(self):
        return F'{self.date} ({self.id})'


class BooleanFilterModel(models.Model):
    is_true = models.BooleanField(null=True)

    @property
    def prop_is_true(self):
        return self.is_true

    def __str__(self):
        return F'{self.is_true} ({self.id})'


class CharFilterModel(models.Model):
    name = models.CharField(max_length=32)

    @property
    def prop_name(self):
        return self.name

    def __str__(self):
        return F'{self.name} ({self.id})'


class ChoiceFilterModel(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number} ({self.id})'


class DateFilterModel(models.Model):
    date = models.DateField()

    @property
    def prop_date(self):
        return self.date

    def __str__(self):
        return F'{self.date} ({self.id})'


class DateFromToRangeFilterModel(models.Model):
    date = models.DateField()
    date_time = models.DateTimeField()

    @property
    def prop_date(self):
        return self.date

    @property
    def prop_date_time(self):
        return self.date_time

    def __str__(self):
        return F'ID: ({self.id}) ---Date: "{self.date}" --- DateTime: "{self.date_time}"'


class DateRangeFilterModel(models.Model):
    date = models.DateField()
    date_time = models.DateTimeField()

    @property
    def prop_date(self):
        return self.date

    @property
    def prop_date_time(self):
        return self.date_time

    def __str__(self):
        return F'ID: ({self.id}) ---Date: "{self.date}" --- DateTime: "{self.date_time}"'


class DateTimeFilterModel(models.Model):
    date_time = models.DateTimeField()

    @property
    def prop_date_time(self):
        return self.date_time

    def __str__(self):
        return F'{self.date_time} ({self.id})'


class DateTimeFromToRangeFilterModel(models.Model):
    date_time = models.DateTimeField()

    @property
    def prop_date_time(self):
        return self.date_time

    def __str__(self):
        return F'{self.date_time} ({self.id})'


class DurationFilterModel(models.Model):
    duration = models.DurationField()

    @property
    def prop_duration(self):
        return self.duration

    def __str__(self):
        return F'{self.duration} ({self.id})'


class IsoDateTimeFilterModel(models.Model):
    date_time = models.DateTimeField()

    @property
    def prop_date_time(self):
        return self.date_time

    def __str__(self):
        return F'{self.date_time} ({self.id})'


class IsoDateTimeFromToRangeFilterModel(models.Model):
    date_time = models.DateTimeField()

    @property
    def prop_date_time(self):
        return self.date_time

    def __str__(self):
        return F'{self.date_time} ({self.id})'


class LookupChoiceFilterModel(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number} ({self.id})'


class ModelChoiceFilterRelatedModel(models.Model):
    text = models.CharField(max_length=32)

    @property
    def prop_text(self):
        return self.text

    def __str__(self):
        return F'{self.text} ({self.id})'


class ModelChoiceFilterModel(models.Model):
    number = models.IntegerField(null=True)
    related = models.ForeignKey(ModelChoiceFilterRelatedModel, on_delete=models.CASCADE, related_name='related_models')

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'Related Key: {self.related} - {self.number} ({self.id})'


class MultipleChoiceFilterModel(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number} ({self.id})'


class NumberFilterModel(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number}'


class OrderingFilterModel(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    age = models.IntegerField()

    @property
    def prop_age(self):
        return self.age

    @property
    def prop_username(self):
        return self.username

    @property
    def prop_first_name(self):
        return self.first_name

    @property
    def prop_last_name(self):
        return self.last_name

    def __str__(self):
        return F'{self.username} - {self.last_name}, {self.first_name}, {self.age} ({self.id})'


class RangeFilterModel(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number}'


class TimeFilterModel(models.Model):
    time = models.TimeField()

    @property
    def prop_time(self):
        return self.time

    def __str__(self):
        return F'{self.time} ({self.id})'


class TimeRangeFilterModel(models.Model):
    time = models.TimeField()

    @property
    def prop_time(self):
        return self.time

    def __str__(self):
        return F'{self.time} ({self.id})'


class TypedChoiceFilterModel(models.Model):
    text = models.CharField(max_length=32)

    @property
    def prop_text(self):
        return self.text

    def __str__(self):
        return F'{self.text} ({self.id})'


class TypedMultipleChoiceFilterModel(models.Model):
    text = models.CharField(max_length=32)

    @property
    def prop_text(self):
        return self.text

    def __str__(self):
        return F'{self.text} ({self.id})'


class UUIDFilterModel(models.Model):
    uuid = models.UUIDField()

    @property
    def prop_uuid(self):
        return self.uuid

    def __str__(self):
        return F'{self.uuid} ({self.id})'


class VolumeTestModel(models.Model):
    date = models.DateField()
    is_true = models.BooleanField(null=True)
    number = models.IntegerField(null=True)
    text = models.CharField(max_length=32)

    @property
    def prop_date(self):
        return self.date

    @property
    def prop_is_true(self):
        return self.is_true

    @property
    def prop_number(self):
        return self.number

    @property
    def prop_text(self):
        return self.text

    def __str__(self):
        return F'{self.number} - "{self.text}" - "{self.is_true}" - "{self.date}" - ({self.id})'


class MultiFilterTestModel(models.Model):
    date = models.DateField(null=True)
    date_time = models.DateTimeField(null=True)
    is_true = models.BooleanField(null=True)
    number = models.IntegerField(null=True)
    text = models.CharField(max_length=32)

    @property
    def prop_date(self):
        return self.date

    @property
    def prop_date_time(self):
        return self.date_time

    @property
    def prop_is_true(self):
        return self.is_true

    @property
    def prop_number(self):
        return self.number

    @property
    def prop_text(self):
        return self.text

    def __str__(self):
        return F'{self.number} - "{self.text}" - "{self.is_true}" - "{self.date}" - "{self.date_time}" - ({self.id})'


class BenchmarkTestModel(models.Model):
    date = models.DateField(null=True)
    date_time = models.DateTimeField(null=True)
    iso_date_time = models.DateTimeField(null=True)
    time = models.TimeField(null=True)
    is_true = models.BooleanField(null=True)
    number = models.IntegerField(null=True)
    text = models.CharField(max_length=32)
    duration = models.DurationField(null=True)
    uuid = models.UUIDField(null=True)

    @property
    def prop_date(self):
        return self.date

    @property
    def prop_date_time(self):
        return self.date_time

    @property
    def prop_iso_date_time(self):
        return self.iso_date_time

    @property
    def prop_time(self):
        return self.time

    @property
    def prop_is_true(self):
        return self.is_true

    @property
    def prop_number(self):
        return self.number

    @property
    def prop_text(self):
        return self.text

    @property
    def prop_duration(self):
        return self.duration

    @property
    def prop_uuid(self):
        return self.uuid

    def __str__(self):
        return (F'{self.number} - "{self.text}" - "{self.is_true}" - "{self.date}" - "{self.date_time}" - '
                F'"{self.iso_date_time}" - "{self.time}" - "{self.duration}" - "{self.uuid}"" ({self.id})')


############### POSTGRESQL Specific Models ###############

class PostgreSQLModel(models.Model):
    class Meta:
        abstract = True
        required_db_vendor = 'postgresql'


class NumericRangeFilterModel(PostgreSQLModel):
    try:
        postgres_int_range = IntegerRangeField(blank=True, null=True)
        postgres_decimal_range = DecimalRangeField(blank=True, null=True)
    except NameError:
        pass

    @property
    def prop_postgres_int_range(self):
        return self.postgres_int_range

    @property
    def prop_postgres_decimal_range(self):
        return self.postgres_decimal_range

    def __str__(self):
        return F'{self.postgres_int_range} - {self.prop_postgres_decimal_range} ({self.id})'
