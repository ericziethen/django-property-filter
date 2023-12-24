"""Utility functionality."""

import logging
import os
import sqlite3

from functools import reduce
from operator import or_

from django.db import connection
from django.db.models import Case, When, Q
from django.db.utils import OperationalError


def get_db_vendor():
    """Get the vendor of the Database used."""
    return connection.vendor


def get_db_version():
    """Get the version of the database used."""
    if get_db_vendor() == 'sqlite':
        return sqlite3.sqlite_version
    return 'Unknown'


def convert_int_list_to_range_lists(int_list, *, sort_list=True):
    """
    Convert a list of numbers to ranges and returns a list of tuples representing the ranges.

    Single numbers will be represented as (3, 3), while ranges will be (4, 8)
    """
    # Build a list of lists
    range_list = []
    working_list = int_list
    if sort_list:
        working_list = sorted(int_list)

    for num in working_list:
        if range_list:
            # Check if Part of range
            if range_list[-1][1] + 1 == num:  # Continuing a range
                range_list[-1][1] = num  # Update Range End
            else:  # Not continuing range
                range_list.append([num, num])
        else:
            range_list.append([num, num])

    # Convert to a list of tuples, could do with list of lists but not really any real overhead
    range_list = [(elem[0], elem[1]) for elem in range_list]

    return range_list


def get_max_params_for_db():
    """Get the allowed number of maximum parameters for the database used, or None if no limit."""
    max_params = None

    if 'USER_DB_MAX_PARAMS' in os.environ:
        user_limit = os.environ['USER_DB_MAX_PARAMS']
        try:
            max_params = int(user_limit)
        except ValueError:
            logging.error(F'Invalid Environment Variable "USER_DB_MAX_PARAMS", int expected but got "{user_limit}".')

    if max_params is None and get_db_vendor() == 'sqlite':
        max_params = 999

    return max_params


def sort_range_list(range_list, *, descending=True):
    """Sorts the given list of ranges based on range size. Descending by default."""

    def compare_range(iterable):
        return abs(iterable[1] - iterable[0]) + 1

    range_list.sort(key=compare_range, reverse=descending)  # Can't return sort() directly, would return None,
    return range_list


def build_limited_filter_expr(pk_list, max_params):
    """Build the filter expression for the limited pk list."""
    # Create the Filter Query with list of ranges and in list based on
    # https://stackoverflow.com/questions/44067134/django-query-an-unknown-number-of-multiple-date-ranges

    # Just go until we used up max_params parameters
    in_range_list = []      # Each entry takes up 2 parameters
    in_list = set()         # Each entry takes up 1 parameter

    params_used = 0

    for entry in sort_range_list(convert_int_list_to_range_lists(pk_list), descending=True):
        if entry[0] == entry[1] or params_used + 1 >= max_params:  # single item or space for only 1 param
            in_list.add(entry[0])
            params_used += 1
        else:  # Range item and enough space for whole range
            in_range_list.append(Q(pk__range=[entry[0], entry[1]]))
            params_used += 2

        if params_used >= max_params:
            break

    # Combine the range__ and in__ queries
    in_range_list.append(Q(pk__in=in_list))

    # Create the Filter Expression
    range_filter_expr = reduce(or_, in_range_list, Q())

    return range_filter_expr


def filter_qs_by_pk_list(queryset, pk_list, *, preserve_order=None):
    """Filter the given queryset by the given list of primary keys.

    Our current approach to use "pk__in" has a big drawback in sqlite where by default
    we can only have 999 or 32766 (depending on version) parameters, i.e. if the result is more than that it will fail,

    For details see
    https://www.sqlite.org/limits.html#:~:text=To%20prevent%20excessive%20memory%20allocations,0.
    9. Maximum Number Of Host Parameters In A Single SQL Statement
    """
    result_qs = queryset.filter(pk__in=pk_list)

    # Only evaluate if we know how to limit the list
    # e.g. For sqlite we know the default limits per version, if we exceed those we can limit how much we return.
    # For other DBs we currently don't know so if there is a limit we just let the exception be passed on

    max_params = get_max_params_for_db()
    if max_params is not None and max_params < len(pk_list):
        try:
            # Evaluate the Result
            result_qs.count()
        except OperationalError:
            if preserve_order:
                # Only do 1/3 of the items to be able to preserve the order
                items_left = int(max_params / 3)
                limited_pk_list = set()

                for entry in preserve_order:
                    if items_left <= 0:
                        break

                    if entry in pk_list:
                        limited_pk_list.add(entry)
                        items_left -= 1
                preserve_order = limited_pk_list  # Order preserved for limited pks
                result_qs = queryset.filter(pk__in=limited_pk_list)

                logging.warning('Limiting the Max SQL Parameters to be able to preserve the filter order')

            else:
                range_filter_expr = build_limited_filter_expr(pk_list, max_params)
                result_qs = queryset.filter(range_filter_expr)

            logging.warning(F'Only returning the first {result_qs.count()} items because of max parameter '
                            F'limitations of Database "{get_db_vendor()}"')

    if preserve_order:
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(preserve_order)])
        result_qs = result_qs.order_by(preserved)

    return result_qs


def get_value_for_db_field(obj, field_str):
    """Lookup a model field or property."""
    def get_attr_val_recursive(obj, sub_list):
        if obj is None:
            return None
        found_value = getattr(obj, sub_list[0])
        if len(sub_list) == 1:
            return found_value

        return get_attr_val_recursive(found_value, sub_list[1:])

    return get_attr_val_recursive(obj, field_str.split('__'))


def compare_by_lookup_expression(  # pylint: disable=too-many-branches,too-many-statements
        lookup_expr, lookup_value, property_value):
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

    # Postgres Ranges exclude the Upper Boundary for Decimal Types, Might Impact us here
    elif lookup_expr == 'postgres_range_exact':
        result = property_value == lookup_value
    elif lookup_expr == 'postgres_range_contains':
        if property_value:
            if lookup_value.start is None:
                result = property_value.stop == lookup_value.stop
            elif lookup_value.stop is None:
                result = property_value.start == lookup_value.start
            else:
                result = ((property_value.start is None or property_value.start <= lookup_value.start) and
                          (property_value.stop is None or property_value.stop >= lookup_value.stop))
    elif lookup_expr == 'postgres_range_contained_by':
        if property_value:
            if lookup_value.start is None:
                result = property_value.stop <= lookup_value.stop
            elif lookup_value.stop is None:
                result = property_value.start >= lookup_value.start
            elif property_value.start is None:
                result = lookup_value.start is None and property_value.stop == lookup_value.stop
            elif property_value.stop is None:
                result = lookup_value.stop is None and property_value.start == lookup_value.start
            else:
                result = ((property_value.start >= lookup_value.start) and
                          (property_value.stop <= lookup_value.stop))
    elif lookup_expr == 'postgres_range_overlap':  # start is included, end is excluded
        # Check if the ranges are not outside of each other instead if defining the actual overlap
        if property_value:
            if property_value.start is None:
                result = lookup_value.start is None or lookup_value.start < property_value.stop
            elif lookup_value.start is None:
                result = property_value.start is None or property_value.start < lookup_value.stop
            elif property_value.stop is None:
                result = lookup_value.stop is None or lookup_value.stop > property_value.start
            elif lookup_value.stop is None:
                result = property_value.stop is None or property_value.stop > lookup_value.start
            else:
                result = not (property_value.start >= lookup_value.stop or lookup_value.start >= property_value.stop)
    elif lookup_expr == 'postgres_range_startwith':
        if property_value:
            result = property_value.start == lookup_value
    elif lookup_expr == 'postgres_range_endwith':
        if property_value:
            result = property_value.stop == lookup_value

    logging.debug(F'property value: "{property_value}", expr: "{lookup_expr}", value: '
                  F'"{lookup_value}" ({type(lookup_value)}) ({type(property_value)}), result: "{result}"')

    return result


def strtobool(val):  # Taken from python directly, as suggested in PEP 632 – Deprecate distutils module
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    if val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0

    raise ValueError(F"invalid truth value {val}")


def convert_value_to_type(target_type, value):
    """Convert the given value to the given type, return the value if can't convert."""
    if (target_type == bool) and (isinstance(value, str)):
        return bool(strtobool(value))

    return target_type(value)
