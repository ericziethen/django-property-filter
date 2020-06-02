# Django Property Filter

Django-property-filter is an extension to [django-filter](https://pypi.org/projhttps://pypi.org/project/django-filter/ect/django-filter/) and provides functionality to filter querysets by class properties.

It does so by providing sub-classes for Filters and Filtersets to keep existing django-filter functionality.

<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/django-property-filter.svg'></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/django-property-filter.svg'></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://travis-ci.com/ericziethen/django-property-filter.svg?branch=master'></td>
        <td>Coverage</td>
        <td><img src='https://codecov.io/gh/ericziethen/django-property-filter/branch/master/graph/badge.svg'></td>
    </tr>
    <tr>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/django-property-filter.svg'></td>
        <td>Implementation</td>
        <td><img src='https://img.shields.io/pypi/implementation/django-property-filter.svg'></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><img src='https://img.shields.io/pypi/status/django-property-filter.svg'></td>
        <td>Downloads</td>
        <td><img src='https://img.shields.io/pypi/dm/django-property-filter.svg'></td>
    </tr>
    <tr>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/django-property-filter.svg'></td>
    </tr>
</table>

## Requirements

* Python 3.8
* Django-filter 2.20

## Installation

Install using pip:

```python
pip install django-property-filter
```

Then add 'django_property_filter' to your INSTALLED_APPS.

```python
INSTALLED_APPS = [
    ...
    'django_property_filter',
]
```

## Usage

### Example Model

Our Model

```python
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
```

### Implicit Filter Creation

If we want to filter by discounted price as well as number of books in a series,
which both are properties and not fields in the database, we would do the
following.::

```python
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
```

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
        If the property is on a related Model it should be separated by ".",
        and can span multiple levels e.g. fk.fk.fk.property
    2.) The specific Property Filter to use.
        This is necessary since it can't be determined what the return type
        of the property will be in all cases
    3.) The list of lookup expressions.

### Explicit Filter Creation

It is also possible to create Filters explicitely.
To do this we can either use FilterSet or PropertyFilterSet.

Using Filterset::

```python
from django_filters import FilterSet
from django_property_filter import PropertyNumberFilter

class BookFilterSet(FilterSet):
    prop_number = PropertyNumberFilter(property_fld_name='discounted_price', lookup_expr='gte')

    class Meta:
        model = NumberClass
        fields = ['prop_number']
```

This creates a "greater than or equel" filter for the discounted_price property

The same can be achieved using a PropertyFilterSet::

```python
from django_property_filter import PropertyNumberFilter, PropertyFilterSet

class BookFilterSet(PropertyFilterSet):
    prop_number = PropertyNumberFilter(property_fld_name='discounted_price', lookup_expr='gte')

    class Meta:
        model = NumberClass
        fields = ['prop_number']
```

## Development

# Run the Django Test Project to see the filters in action

* go to "tests\django_test_proj"
* run "python manage.py runserver"

