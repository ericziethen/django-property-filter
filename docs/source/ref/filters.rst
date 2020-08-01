
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

.. _invalid-type-comparison:

Invalid Type Comparison
-----------------------

When the selected Filter Type and comparison is incompatible with the type the
the property returns that queryset entry will not be a match and an error is
logged similar to

    Error during comparing property value "15" with filter value "text" with error: "'<' not supported between instances of 'int' and 'str'"

.. _core-arguments:

Core Arguments
--------------

``field_name``
~~~~~~~~~~~~~~

The name of the property to lookup.

This can be

    1.) Property directly on the model e.g. "field_name='my_property'"

    2.) A Related field property e.g. "field_name='related__my_property'"
        which can span as many models as are related

``lookup_expr``
~~~~~~~~~~~~~~~

The lookup expression to filter against.
The default lookup expression when not specified will be 'exact' if the filter supports it.
Some filters only support 'range' and this will be the default.

Unmapped Filters
----------------

``ModelChoiceFilter``
~~~~~~~~~~~~~~~~~~~~~

Because ModelChoiceFilter works directly on a models foreign keys, there is no
need for a property filter.

``ModelMultipleChoiceFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because ModelMultipleChoiceFilter works directly on a models foreign keys, there
is no need for a property filter.

Property Filter Classes
-----------------------

``PropertyAllValuesFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of AllValuesFilter for property filtering.

For supported lookups see :ref:`base_lookups`

``PropertyAllValuesMultipleFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of AllValuesMultipleFilter for property filtering.

For supported lookups see :ref:`base_lookups`

``PropertyBaseCSVFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of BaseCSVFilter for property filtering

Supported lookups are 'in' and 'range'

``PropertyBaseInFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of BaseInFilter for property filtering

Supported lookup is 'in'

``PropertyBaseRangeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of BaseRangeFilter for property filtering

Supported lookup is 'range'

``PropertyBooleanFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of BooleanFilter for property filtering

Supported lookups are 'exact' and 'isnull'

``PropertyCharFilter``
~~~~~~~~~~~~~~~~~~~~~~

Used instead of CharFilter for property filtering.

For supported lookups see :ref:`base_lookups`

``PropertyChoiceFilter``
~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of CoiceFilter for property filtering.

For supported lookups see :ref:`base_lookups`

Because the choices are passed as arguments this filter can only be created
explicitely. For example::

    number = PropertyChoiceFilter(field_name='number', lookup_expr='exact', choices=LOOKUP_CHOICES)

``PropertyDateFilter``
~~~~~~~~~~~~~~~~~~~~~~

Used instead of DateFilter for property filtering

Supported lookups are 'exact', 'gt', 'gte', 'lt' and 'lte'

``PropertyDateFromToRangeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of DateFromToRangeFilter for property filtering

Supported lookup is 'range'

``PropertyDateRangeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of DateRangeFilter for property filtering

Supported lookup is 'exact'

``PropertyDateTimeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of DateTimeFilter for property filtering

Supported lookups are 'exact', 'gt', 'gte', 'lt' and 'lte'

``PropertyDateTimeFromToRangeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of DateTimeFromToRangeFilter for property filtering

Supported lookup is 'range'

``PropertyDurationFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of DurationFilter for property filtering

Supported lookups are 'exact', 'gt', 'gte', 'lt' and 'lte'

``PropertyIsoDateTimeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of IsoDateTimeFilter for property filtering

Supported lookups are 'exact', 'gt', 'gte', 'lt' and 'lte'

``PropertyIsoDateTimeFromToRangeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of IsoDateTimeFromToRangeFilter for property filtering

Supported lookup is 'range'

``PropertyLookupChoiceFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of LookupChoiceFilter for property filtering.

For supported lookups see :ref:`base_lookups`

Because the lookup choices are passed as arguments this filter can only be
created explicitely. For example::

    number = PropertyMultipleChoiceFilter(field_name='number', lookup_choices=['exact', 'gt'])

or for all available choices::

    number = PropertyMultipleChoiceFilter(field_name='number')

``PropertyMultipleChoiceFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of MultipleChoiceFilter for property filtering.

For supported lookups see :ref:`base_lookups`

Because the choices are passed as arguments this filter can only be created
explicitely. For example::

    number = PropertyMultipleChoiceFilter(field_name='number', lookup_expr='exact', choices=LOOKUP_CHOICES)

``PropertyNumberFilter``
~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of NumberFilter for property filtering.

Supported lookups are 'exact', 'contains', 'gt', 'gte', 'lt', 'lte', 'startswith' and 'endswith'

``PropertyRangeFilter``
~~~~~~~~~~~~~~~~~~~~~~~

Used instead of RangeFilter for property filtering

Supported lookup is 'range'

``PropertyTimeFilter``
~~~~~~~~~~~~~~~~~~~~~~

Used instead of TimeFilter for property filtering

Supported lookups are 'exact', 'gt', 'gte', 'lt' and 'lte'

``PropertyTimeRangeFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of TimeRangeFilter for property filtering

Supported lookup is 'range'

``PropertyTypedChoiceFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of TypedChoiceFilter for property filtering.

For supported lookups see :ref:`base_lookups`

Because the choices are passed as arguments this filter can only be created
explicitely. For example::

    number = PropertyTypedChoiceFilter(field_name='number_str', lookup_expr='exact', choices=NUMBER_LIST, coerce=int)

``PropertyTypedMultipleChoiceFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used instead of TypedMultipleChoiceFilter for property filtering.

For supported lookups see :ref:`base_lookups`

Because the choices are passed as arguments this filter can only be created
explicitely. For example::

    number = PropertyTypedMultipleChoiceFilter(field_name='number_str', lookup_expr='exact', choices=NUMBER_LIST, coerce=int)

``PropertyUUIDFilter``
~~~~~~~~~~~~~~~~~~~~~~

Used instead of UUIDFilter for property filtering

Supported lookup is 'exact'
