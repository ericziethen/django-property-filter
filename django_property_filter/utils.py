"""Utility functionality."""

from django.db.models import Case, When


def filter_qs_by_pk_list(queryset, pk_list):


    '''
    https://www.sqlite.org/limits.html#:~:text=To%20prevent%20excessive%20memory%20allocations,0.

    9. Maximum Number Of Host Parameters In A Single SQL Statement

    A host parameter is a place-holder in an SQL statement that is filled in using one of the sqlite3_bind_XXXX() interfaces. Many SQL programmers are familiar with using a question mark ("?") as a host parameter. SQLite also supports named host parameters prefaced by ":", "$", or "@" and numbered host parameters of the form "?123".

    Each host parameter in an SQLite statement is assigned a number. The numbers normally begin with 1 and increase by one with each new parameter. However, when the "?123" form is used, the host parameter number is the number that follows the question mark.

    SQLite allocates space to hold all host parameters between 1 and the largest host parameter number used. Hence, an SQL statement that contains a host parameter like ?1000000000 would require gigabytes of storage. This could easily overwhelm the resources of the host machine. To prevent excessive memory allocations, the maximum value of a host parameter number is SQLITE_MAX_VARIABLE_NUMBER, which defaults to 999 for SQLite versions prior to 3.32.0 (2020-05-22) or 32766 for SQLite versions after 3.32.0.

    The maximum host parameter number can be lowered at run-time using the sqlite3_limit(db,SQLITE_LIMIT_VARIABLE_NUMBER,size) interface.
    '''
    # TODO - Either detect the max from SQL if possible or use 999 to be backwards compatible

    #return queryset.filter(pk__in=pk_list)
    print('#################### BEFORE FILTER #######################')
    #qs = queryset.filter(pk__in=pk_list)
    print('pk_list[:600]',pk_list[:600])
    qs = queryset.filter(pk__in=pk_list[:499]) | queryset.filter(pk__in=pk_list[600:1101])
    print('qs.query', queryset.query)
    print('#################### AFTER FILTER #######################')
    return qs


def sort_queryset(sort_property, queryset):
    """Sort the queryset by the given property name. "-" for descending is supported."""
    # Identify the sort order
    descending = False
    if sort_property.startswith('-'):
        descending = True
        sort_property = sort_property[1:]

    # Build a list of pk and value, this might become very large depending on data type
    value_list = []
    for obj in queryset:
        property_value = get_value_for_db_field(obj, sort_property)
        value_list.append((obj.pk, property_value))

    # Sort the list of tuples
    value_list = sorted(value_list, key=lambda x: x[1], reverse=descending)

    # Get a list of sorted primary keys
    value_list = [entry[0] for entry in value_list]

    # Sort the Queryset
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(value_list)])
    queryset = filter_qs_by_pk_list(queryset, value_list).order_by(preserved)

    # TODO - REVIEW filter for large number
    # TODO - WE SHOULD HAVE A FILTER QS BY PK TO REUSE IT
    # https://code.djangoproject.com/ticket/17788


    return queryset


def get_value_for_db_field(obj, field_str):
    """Lookup a model field or property."""
    def get_attr_val_recursive(obj, sub_list):
        if len(sub_list) == 1:
            return getattr(obj, sub_list[0])

        new_object = getattr(obj, sub_list[0])
        return get_attr_val_recursive(new_object, sub_list[1:])

    return get_attr_val_recursive(obj, field_str.split('__'))


def compare_by_lookup_expression(lookup_expr, lookup_value, property_value):  # pylint: disable=too-many-branches
    """Compare Lookup Expressions."""
    result = False

    # Do the Comparison
    if lookup_expr == 'exact':
        result = str(property_value) == str(lookup_value)
    elif lookup_expr == 'iexact':
        result = str(property_value).lower() == str(lookup_value).lower()
    elif lookup_expr == 'contains':
        result = str(lookup_value) in str(property_value)
    elif lookup_expr == 'icontains':
        result = str(lookup_value).lower() in str(property_value).lower()
    elif lookup_expr == 'gt' and property_value is not None and lookup_value is not None:
        result = property_value > lookup_value
    elif lookup_expr == 'gte' and property_value is not None and lookup_value is not None:
        result = property_value >= lookup_value
    elif lookup_expr == 'lt' and property_value is not None and lookup_value is not None:
        result = property_value < lookup_value
    elif lookup_expr == 'lte' and property_value is not None and lookup_value is not None:
        result = property_value <= lookup_value
    elif lookup_expr == 'startswith':
        result = str(property_value).startswith(str(lookup_value))
    elif lookup_expr == 'istartswith':
        result = str(property_value).lower().startswith(str(lookup_value).lower())
    elif lookup_expr == 'endswith':
        result = str(property_value).endswith(str(lookup_value))
    elif lookup_expr == 'iendswith':
        result = str(property_value).lower().endswith(str(lookup_value).lower())
    elif lookup_expr == 'isnull':
        result = (lookup_value and property_value is None) or (not lookup_value and property_value is not None)
    elif lookup_expr == 'range' and property_value is not None and lookup_value is not None:
        result = lookup_value.start <= property_value <= lookup_value.stop
    elif lookup_expr == 'in':
        result = property_value in lookup_value

    return result
