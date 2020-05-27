

def get_value_for_db_field(obj, field_str):

    def get_attr_val_recursive(obj, sub_list):
        if len(sub_list) == 1:
            return getattr(obj, sub_list[0])

        new_object = getattr(obj, sub_list[0])
        return get_attr_val_recursive(new_object, sub_list[1:])

    return get_attr_val_recursive(obj, field_str.split('.'))


def compare_by_lookup_expression(lookup_expr, candidate_value, lookup_value):
    if lookup_expr == 'exact':
        return str(lookup_value) == str(candidate_value)
    elif lookup_expr == 'iexact':
        return str(lookup_value).lower() == str(candidate_value).lower()
    elif lookup_expr == 'contains':
        return str(candidate_value) in str(lookup_value)
    elif lookup_expr == 'icontains':
        return str(candidate_value).lower() in str(lookup_value).lower()
    elif lookup_expr == 'gt':
        return candidate_value > lookup_value
    elif lookup_expr == 'gte':
        return candidate_value >= lookup_value
    elif lookup_expr == 'lt':
        return candidate_value < lookup_value
    elif lookup_expr == 'lte':
        return candidate_value <= lookup_value
    elif lookup_expr == 'startswith':
        return str(lookup_value).startswith(str(candidate_value))
    elif lookup_expr == 'istartswith':
        return str(lookup_value).lower().startswith(str(candidate_value).lower())
    elif lookup_expr == 'endswith':
        return str(lookup_value).endswith(str(candidate_value))
    elif lookup_expr == 'iendswith':
        return str(lookup_value).lower().endswith(str(candidate_value).lower())

    return False
