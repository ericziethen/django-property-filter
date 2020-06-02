"""Utility functionality."""


def get_value_for_db_field(obj, field_str):
    """Lookup a model field or property."""
    def get_attr_val_recursive(obj, sub_list):
        if len(sub_list) == 1:
            return getattr(obj, sub_list[0])

        new_object = getattr(obj, sub_list[0])
        return get_attr_val_recursive(new_object, sub_list[1:])

    return get_attr_val_recursive(obj, field_str.split('.'))


def compare_by_lookup_expression(lookup_expr, lookup_value, compare_value):  # pylint: disable=too-many-branches
    """Compare Lookup Expressions."""
    # Handle Special case if only 1 case of range given
    if lookup_expr == 'range':
        if lookup_value[0] is None:
            lookup_expr = 'lte'
            lookup_value = lookup_value[1]
        elif lookup_value[1] is None:
            lookup_expr = 'gte'
            lookup_value = lookup_value[0]

    print('compare_by_lookup_expression()', lookup_expr, lookup_value, compare_value)

    result = False

    # Do the Comparison
    if lookup_expr == 'exact':
        result = str(compare_value) == str(lookup_value)
    elif lookup_expr == 'iexact':
        result = str(compare_value).lower() == str(lookup_value).lower()
    elif lookup_expr == 'contains':
        result = str(lookup_value) in str(compare_value)
    elif lookup_expr == 'icontains':
        result = str(lookup_value).lower() in str(compare_value).lower()
    elif lookup_expr == 'gt' and compare_value is not None and lookup_value is not None:
        result = compare_value > lookup_value
    elif lookup_expr == 'gte' and compare_value is not None and lookup_value is not None:
        result = compare_value >= lookup_value
    elif lookup_expr == 'lt' and compare_value is not None and lookup_value is not None:
        result = compare_value < lookup_value
    elif lookup_expr == 'lte' and compare_value is not None and lookup_value is not None:
        result = compare_value <= lookup_value
    elif lookup_expr == 'startswith':
        result = str(compare_value).startswith(str(lookup_value))
    elif lookup_expr == 'istartswith':
        result = str(compare_value).lower().startswith(str(lookup_value).lower())
    elif lookup_expr == 'endswith':
        result = str(compare_value).endswith(str(lookup_value))
    elif lookup_expr == 'iendswith':
        result = str(compare_value).lower().endswith(str(lookup_value).lower())
    elif lookup_expr == 'isnull':
        result = lookup_value is None
    elif lookup_expr == 'range' and compare_value is not None and lookup_value is not None:
        result = lookup_value[0] <= compare_value <= lookup_value[1]
    elif lookup_expr == 'in':
        result = compare_value in lookup_value

    return result
