============================
Additional FilterSet Options
============================

This document provides a guide on using additional PropertyFilterSet features in
addition to FilterSet.

Meta options
------------

- :ref:`property_fields <property_fields>`


.. _property_fields:

Automatic filter generation with ``property_fields``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``PropertyFilterSet`` is capable of automatically generating filters for a 
given clas Properties accessible by the ``model`` or it's related models.

.. code-block:: python

    class BookFilterSet(PropertyFilterSet):

      class Meta:
          model = Book
          exclude = ['price']
          property_fields = [
            ('discounted_price', PropertyNumberFilter, ['lt', 'exact']),
            ('series.book_count.', PropertyNumberFilter, ['gt', 'exact']),
          ]

The "property_fields" is a list of tuples with 3 values.
    1.) The property name. 
        If the property is on a related Model it should be separated by ".",
        and can span multiple levels e.g. fk.fk.fk.property
    2.) The specific Property Filter to use.
        This is necessary since it can't be determined what the return type
        of the property will be in all cases
    3.) The list of lookup expressions.
