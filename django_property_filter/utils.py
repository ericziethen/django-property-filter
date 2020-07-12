"""Utility functionality."""


def get_value_for_db_field(obj, field_str):
    """Lookup a model field or property."""
    def get_attr_val_recursive(obj, sub_list):
        if len(sub_list) == 1:
            return getattr(obj, sub_list[0])

        new_object = getattr(obj, sub_list[0])
        return get_attr_val_recursive(new_object, sub_list[1:])

    return get_attr_val_recursive(obj, field_str.split('.'))


def compare_by_lookup_expression(lookup_expr, lookup_value, property_value):  # pylint: disable=too-many-branches
    """Compare Lookup Expressions."""
    # Handle Special case if only 1 case of range given
    if lookup_expr == 'range':
        if lookup_value.start is None:
            lookup_expr = 'lte'
            lookup_value = lookup_value.stop
        elif lookup_value.stop is None:
            lookup_expr = 'gte'
            lookup_value = lookup_value.start

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
