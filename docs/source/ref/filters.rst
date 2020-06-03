
================
Filter Reference
================

This is a reference document with a list of the filters and their property
specific arguments specific for property filters.

.. _base_lookups:

Supported Base Lookup Expressions
---------------------------------

This is a list lookup expressions supported by all Property Filters unless
excludes specifically.

* 'exact'           -> Matches value exact (case sensitive)
* 'iexact'          -> Matches value exact (case insensitive)
* 'contains'        -> Contains value (case sensitive)
* 'icontains'       -> Contains value (case insensitive)
* 'gt'              -> Greater than
* 'gte'             -> Greater than or equal
* 'lt'              -> Less than
* 'lte'             -> Less than or equal
* 'startswith'      -> Starts with value (case sensitive)
* 'istartswith'     -> Starts with value (case sensitive)
* 'endswith'        -> Ends with value (case sensitive)
* 'iendswith'       -> Ends with value (case sensitive)

.. warning::
    Sqlite by default uses case insensitive text comparison, so e.g.
    'exact' and 'iexact' will giv the same result.
    Even if turning on case sensitivity with PRAGMA case_sensitive_like,
    both still result in the same result.

    Django-property-filter will behave as normally expected in this case and
    will correctly check for case sensitivity.


.. _core-arguments:

Core Arguments
--------------

``property_fld_name``
~~~~~~~~~~~~~~~~~~~~~

The name of the property to lookup.

This can be

    1.) Property directly on the model e.g. "property_fld_name='my_property'"

    2.) A Related field property e.g. "property_fld_name='related.my_property'"
        which can span as many models as are related

Property Filter Classes
-----------------------

``PropertyNumberFilter``
~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of NumberFilter for property filtering.

For supported lookups see :ref:`base_lookups`

``PropertyBooleanFilter``
~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of BooleanFilter for property filtering

Supported lookups are "exact" and "isnull"
