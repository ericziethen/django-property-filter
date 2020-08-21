===============
Getting Started
===============

Django-property-filter provides extended functionality to django-filter to allow
filtering by class properties by providing new Sub Classes to django-filter's
Filter and Filterset classes.

All existing django-filter functionality is still working as before.

Example Model
-------------

Our Model::

    from django.db import models

    class BookSeries(models.Model):
        name = models.CharField(max_length=255)

        @property
        def book_count(self):
          return Book.objects.filter(series=self).count()

    class Book(models.Model):
        title = models.CharField(max_length=255)
        price = models.DecimalField()
        discount_percentage = models.IntegerField()
        author = models.TextField()
        series = models.ForeignKey(BookSeries)

        @property
        def discounted_price(self):
          return self.price * self.discount_percentage \ 100


Implicit Filter Creation
------------------------

If we want to filter by discounted price as well as number of books in a series,
which both are properties and not fields in the database, we would do the
following.::

    from django_property_filter import (
      PropertyFilterSet,
      PropertyNumberFilter
    )

    class BookFilterSet(PropertyFilterSet):

      class Meta:
          model = Book
          exclude = ['price']
          property_fields = [
            ('discounted_price', PropertyNumberFilter, ['lt', 'exact']),
            ('series.book_count.', PropertyNumberFilter, ['gt', 'exact']),
          ]

This will create 4 Filters
    1.) A "less than" and an "exact" filter for the "discounted_price" property
        of the Book Model
    2.) A "greater than" and an "exact" filter for the "book_count" property
        of the related Model "series".

Since PropertyFilterSet is and extension to django-filter's Filterset which
requires either the Meta attribute "fields" or "exclude" to be set we excluded
the "price" field. If we had instead used::
    fields = ['price']

It would also have created an "exact" filter for the book price.

The only difference to using a normal FilterSet from django-filter is the
"property_fields" field.

The "property_fields" is a list of tuples with 3 values.
    1.) The property name. 
        If the property is on a related Model it should be separated by "__",
        and can span multiple levels e.g. fk__fk__fk__property
    2.) The specific Property Filter to use.
        This is necessary since it can't be determined what the return type
        of the property will be in all cases
    3.) The list of lookup expressions.

Explicit Filter Creation
------------------------

It is also possible to create Filters explicitely::

    from django_property_filter import PropertyNumberFilter, PropertyFilterSet

    class BookFilterSet(PropertyFilterSet):
        prop_number = PropertyNumberFilter(field_name='discounted_price', lookup_expr='gte')

        class Meta:
            model = NumberClass
            fields = ['prop_number']

This creates a "greater than or equel" filter for the discounted_price property
