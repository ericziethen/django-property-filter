========
Overview
========

Overview
--------

Django-property-filter provides an extenstion to `django-filter <https://django-filter.readthedocs.io/>`_.
It extend's django-filter's classes to provide additional support for filtering
`django <https://www.djangoproject.com/>`_ models by properties.

The aim is to provide identical (where possible) functionality for properties
as django-filter does for database fields.
For this the new classes directly inherit their django-filter counterpart's
features and the setup and configuration is aimed to be the same.

This means that the `django-filter documentation <https://django-filter.readthedocs.io/en/master/>`_
can be applied to django-property-filter as well.

For example django-filter uses a class NumberFilter and django-property-filter
extends it and creates PropertyNumberFilter supporting the same functionality
and additional the possibility to filter properties as well.

Because property fields are not part of database tables they cannot be queried
directly with sql and are therefore not natively supported by django and
django-filter.

Django-property-filter also provides a filterset that can handle filters
and property filters together.

How it works
------------

Where django-filter directly applies the filtering to the queryset,
django-property-filter can't do that because the properties are not database
fields.
To workaround this, all entries are compared in memory against all specified
filters resulting in a list of matching primary keys.
This list can then be used to filter the original queryset like this::

    queryset.filter(pk__in=filtered_pk_list)


Because of this the actual filtering is happening in memory of the django
application rather than in sql.
