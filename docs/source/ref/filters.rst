.. _filter-reference:

================
Filter Reference
================

This is a reference document with a list of the filters and their property
specific arguments specific for property filters.

Filter to Property Filter Mapping
---------------------------------

The following tables shows the corresponding Property Filters for Filters from
django-filters.

.. csv-table:: Filter Mapping
    :header-rows: 1

    "AllValuesFilter", "PropertyAllValuesFilter"
    "AllValuesMultipleFilter", "PropertyAllValuesMultipleFilter"
    "BaseCSVFilter", "PropertyBaseCSVFilter"
    "BaseInFilter", "PropertyBaseInFilter"
    "BaseRangeFilter", "PropertyBaseRangeFilter"
    "BooleanFilter", "PropertyBooleanFilter"
    "CharFilter", "PropertyCharFilter"
    "ChoiceFilter", "PropertyChoiceFilter"
    "DateFilter", "PropertyDateFilter"
    "DateFromToRangeFilter", "PropertyDateFromToRangeFilter"
    "DateRangeFilter", "PropertyDateRangeFilter"
    "DateTimeFilter", "PropertyDateTimeFilter"
    "DateTimeFromToRangeFilter", "PropertyDateTimeFromToRangeFilter"
    "DurationFilter", "PropertyDurationFilter"
    "Filter", "Property Filter"
    "IsoDateTimeFilter", "PropertyIsoDateTimeFilter"
    "IsoDateTimeFromToRangeFilter", "PropertyIsoDateTimeFromToRangeFilter"
    "LookupChoiceFilter", "PropertyLookupChoiceFilter"
    "ModelChoiceFilter", "N/A (Not needed because filtering foreign key"
    "ModelMultipleChoiceFilter", "N/A (Not needed because filtering foreign key"
    "MultipleChoiceFilter", "PropertyMultipleChoiceFilter"
    "NumberFilter", "PropertyNumberFilter"
    "NumericRangeFilter", "PropertyNumericRangeFilter"
    "OrderingFilter", "PropertyOrderingFilter"
    "RangeFilter", "PropertyRangeFilter"
    "TimeFilter", "PropertyTimeFilter"
    "TimeRangeFilter", "PropertyTimeRangeFilter"
    "TypedChoiceFilter", "PropertyTypedChoiceFilter"
    "TypedMultipleChoiceFilter", "PropertyTypedMultipleChoiceFilter"
    "UUIDFilter", "PropertyUUIDFilter"


Supported Property Filter Expressions
-------------------------------------

The following tables shows the supported lookup expressions and hightlights
the default  one if none is specified.

.. csv-table:: Supported Expressions
    :header-rows: 1

    "PropertyAllValuesFilter", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyAllValuesMultipleFilter", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyBaseCSVFilter", "**in**, range"
    "PropertyBaseInFilter", "**in**"
    "PropertyBaseRangeFilter", "**range**"
    "PropertyBooleanFilter", "**exact**, isnull"
    "PropertyCharFilter", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyChoiceFilter [2]_", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyDateFilter", "**exact**, gt, gte, lt, lte"
    "PropertyDateFromToRangeFilter", "**range**"
    "PropertyDateRangeFilter", "**exact**"
    "PropertyDateTimeFilter", "**exact**, gt, gte, lt, lte"
    "PropertyDateTimeFromToRangeFilter", "**range**"
    "PropertyDurationFilter", "**exact**, gt, gte, lt, lte"
    "PropertyIsoDateTimeFilter", "**exact**, gt, gte, lt, lte"
    "PropertyIsoDateTimeFromToRangeFilter", "**range**"
    "PropertyLookupChoiceFilter [3]_", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyMultipleChoiceFilter [2]_", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyNumberFilter", "**exact**, contains, gt, gte, lt, lte, startswith, endswith"
    "PropertyNumericRangeFilter [1]_", "**exact**, contains, contained_by, overlap"
    "PropertyOrderingFilter [4]_", "**exact**"
    "PropertyRangeFilter", "**range**"
    "PropertyTimeFilter", "**exact**, gt, gte, lt, lte"
    "PropertyTimeRangeFilter", "**range**"
    "PropertyTypedChoiceFilter [2]_", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyTypedMultipleChoiceFilter [2]_", "**exact**, iexact, contains, icontains, gt, gte, lt, lte, startswith, istartswith, endswith, iendswith"
    "PropertyUUIDFilter", "**exact**"

.. [1] Postgres only
.. [2] Explicit Creation only, choices need to be passed
.. [3] Explicit Creation only, choices need to be passed or all available expressions are choices
.. [4] see `PropertyOrderingFilter`_

.. _base_lookups:

Supported Base Lookup Expressions
---------------------------------

This is a list lookup expressions supported by all Property Filters unless
excludes specifically.

* 'contained_by'    -> Subset of the given value
* 'contains'        -> Contains value (case sensitive)
* 'endswith'        -> Ends with value (case sensitive)
* 'exact'           -> Matches value exact (case sensitive)
* 'gt'              -> Greater than
* 'gte'             -> Greater than or equal
* 'icontains'       -> Contains value (case insensitive)
* 'iendswith'       -> Ends with value (case sensitive)
* 'iexact'          -> Matches value exact (case insensitive)
* 'in'              -> Matches specified list of values or range 
* 'isnull'          -> Is null
* 'istartswith'     -> Starts with value (case sensitive)
* 'lt'              -> Less than
* 'lte'             -> Less than or equal
* 'overlap'         -> Overlapping with the given value
* 'range'           -> Part of the given range
* 'startswith'      -> Starts with value (case sensitive)

.. warning::
    Sqlite by default uses case insensitive text comparison, so e.g.
    'exact' and 'iexact' will give the same result.
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


Appendix
--------

``PropertyOrderingFilter``
--------------------------

Because the field parameters are passed as arguments this filter can only be created
explicitely. For example::

    prop_age = PropertyOrderingFilter(fields=('prop_age', 'prop_age'))

.. warning::
    Sorting is all happening in memory rather than sql.
    Since this filter depends on sorted querysets, the sorting loads the values
    into memory first and therefore can make it an expensive operator.
    Carefull with larger data sets.

    Because of the in memory sorting, sorting is only supported by a single 
    property
