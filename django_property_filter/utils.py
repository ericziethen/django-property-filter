"""Utility functionality."""

from django.db.models import Case, When


def sort_queryset_by_value(value, queryset, *, descending=False):
    # Build a list of pk and value, this might become very large depending on data type
    value_list = []
    for obj in queryset:
        property_value = get_value_for_db_field(obj, value)
        value_list.append((obj.pk, property_value))

    # Sort the list of tuples
    value_list = sorted(value_list, key=lambda x: x[1], reverse=descending)

    # Get a list of sorted primary keys
    value_list = [entry[0] for entry in value_list]

    # Sort the Queryset
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(value_list)])
    queryset = queryset.filter(pk__in=value_list).order_by(preserved)

    return queryset


def sort_queryset(sort_value_list, queryset):
    sort_value = sort_value_list[0]
    descending = False
    if sort_value.startswith('-'):
        descending = True
        sort_value = sort_value[1:]

    return sort_queryset_by_value(sort_value, queryset, descending=descending)


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


    print('compare_by_lookup_expression(lookup_expr, lookup_value, property_value)',
        lookup_expr, lookup_value, property_value)





    return result
