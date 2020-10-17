========
Overview
========

Overview
--------

Django-property-filter is an application adding filtering by class properties
functionality to `django <https://www.djangoproject.com/>`_.

It is inspired by and an extension of the `django-filter <https://django-filter.readthedocs.io/>`_ application.
As such the aim is to provide the same functionality django-filter provides for
database fields but for property fields of django models.

Because property fields are not part of database tables they cannot be queried
directly with sql and are therefore not natively supported by django and
django-filter.

The aim for django-property-filter is to provide a property filter for each
filter available in django-filter.

Django-property-filter will also provide a filterset that can handle filters
and property filters together.

How it works
------------

Where django-filter directly applies the filtering to the queryset,
django-property-filter can't do that because the properties are not database
fields.
To workaround this, all entries are compared in memory against all specified
filters resulting in a list of matching primary keys.
This list can then be used to filter the original queryset like this.

.. code-block:: python

    queryset.filter(pk__in=filtered_pk_list)


Because of this the actual filtering is happening in memory of the django
application rather than in sql.
