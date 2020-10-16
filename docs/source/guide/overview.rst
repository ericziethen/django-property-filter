========
Overview
========

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
