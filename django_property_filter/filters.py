
from django_filters.filters import (
    NumberFilter,
)

from django_filters.utils import verbose_lookup_expr


class PropertyBaseFilterMixin():
    def __init__(self, field_name=None, lookup_expr=None, *, label=None,
                 method=None, distinct=False, exclude=False, property_fld_name, **kwargs):
        label = F'{label} {verbose_lookup_expr(lookup_expr)}'
        self.property_fld_name = property_fld_name
        super().__init__(field_name=field_name, lookup_expr=lookup_expr, label=label,
                         method=method, distinct=distinct, exclude=exclude, **kwargs)


class PropertyNumberFilter(PropertyBaseFilterMixin, NumberFilter):
    pass










