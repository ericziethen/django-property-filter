

def get_value_for_db_field(obj, field_str):

    def get_attr_val_recursive(obj, sub_list):
        if len(sub_list) == 1:
            return getattr(obj, sub_list[0])

        new_object = getattr(obj, sub_list[0])
        return get_attr_val_recursive(new_object, sub_list[1:])

    return get_attr_val_recursive(obj, field_str.split('.'))


def compare_by_lookup_expression(lookup_expr, lookup_value, compare_value):
    # Handle Special case if only 1 case of range given
    if lookup_expr == 'range':
        if lookup_value[0] is None:
            lookup_expr = 'lte'
            lookup_value = lookup_value[1]
        elif lookup_value[1] is None:
            lookup_expr = 'gte'
            lookup_value = lookup_value[0]


    # Do the Comparison
    if lookup_expr == 'exact':
        return str(compare_value) == str(lookup_value)
    elif lookup_expr == 'iexact':
        return str(compare_value).lower() == str(lookup_value).lower()
    elif lookup_expr == 'contains':
        return str(lookup_value) in str(compare_value)
    elif lookup_expr == 'icontains':
        return str(lookup_value).lower() in str(compare_value).lower()
    elif lookup_expr == 'gt':
        return compare_value > lookup_value
    elif lookup_expr == 'gte':
        return compare_value >= lookup_value
    elif lookup_expr == 'lt':
        return compare_value < lookup_value
    elif lookup_expr == 'lte':
        return compare_value <= lookup_value
    elif lookup_expr == 'startswith':
        return str(compare_value).startswith(str(lookup_value))
    elif lookup_expr == 'istartswith':
        return str(compare_value).lower().startswith(str(lookup_value).lower())
    elif lookup_expr == 'endswith':
        return str(compare_value).endswith(str(lookup_value))
    elif lookup_expr == 'iendswith':
        return str(compare_value).lower().endswith(str(lookup_value).lower())
    elif lookup_expr == 'isnull':
        return lookup_value is None
    elif lookup_expr == 'range':
        return lookup_value[0] <= compare_value <= lookup_value[1]
    elif lookup_expr == 'in':
        return compare_value in lookup_value

    return False
